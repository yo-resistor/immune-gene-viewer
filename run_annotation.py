import subprocess
import hashlib
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

def hash_file(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def log_run(stage_name, input_file, input_hash):
    log_path = Path("data/logs.csv")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "run_id": stage_name,
        "timestamp": datetime.now().isoformat(),
        "input_file": str(input_file),
        "input_hash": input_hash
    }

    if log_path.exists():
        df = pd.read_csv(log_path)
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([log_entry])

    df.to_csv(log_path, index=False)

def create_dvc_stage(stage_name, input_file, output_file, patient_id):
    dvcfile = Path("dvc.yaml")
    if dvcfile.exists() and stage_name in dvcfile.read_text():
        print(f"[INFO] Stage '{stage_name}' already exists. Overwriting with --force.")
        force_flag = ["--force"]
    else:
        force_flag = []
        
    cmd = [
        "dvc", "stage", "add",
        "-n", stage_name,
        *force_flag,
        "-d", str(input_file),
        "-o", str(output_file),
        "python", "annotate.py",
        "--input", str(input_file),
        "--output", str(output_file),
        "--patient_id", patient_id
    ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    patient_id = sys.argv[1]
    input_file = Path(f"data/uploads/input_{patient_id}.csv")
    output_file = Path(f"data/outputs/output_{patient_id}.csv")

    input_hash = hash_file(input_file)
    stage_name = f"annotate_{patient_id}"

    create_dvc_stage(stage_name, input_file, output_file, patient_id)
    log_run(stage_name, input_file, input_hash)

    # run the stage after creation
    try:
        subprocess.run(["dvc", "repro", stage_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to run DVC stage {stage_name}: {e}")