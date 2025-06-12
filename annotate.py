import pandas as pd
from pathlib import Path
from datetime import datetime

def annotate_variants(input_path: str, output_dir: str, patient_id: str) -> str:
    """
    Annotates variants and saves output with patient ID and timestamp.

    Parameters:
    - input_path (str): Path to input CSV file with 'Gene' and 'Allele' columns.
    - output_path (str): Path where the annotated CSV will be saved.
    - patient_id (str): Patient unique ID.
    
    Returns:
        str: Path to the output file.
    """
    df = pd.read_csv(input_path)

    def risk_logic(allele):
        if "B*08" in allele:
            return "Very High"
        elif "B" in allele:
            return "High"
        elif "A" in allele:
            return "Moderate"
        else:
            return "Low"

    df["Risk"] = df["Allele"].apply(risk_logic)
    df["PatientID"] = patient_id  # Optional: include ID in file

    # Create timestamped output path
    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    output_filename = f"annotated_{patient_id}_{timestamp}.csv"
    output_path = Path(output_dir) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    return str(output_path)


if __name__ == "__main__":
    import sys
    import subprocess

    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/test_alleles.csv"
    patient_id = sys.argv[2] if len(sys.argv) > 2 else "P000"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "data/outputs"

    output_path = annotate_variants(input_path, output_dir, patient_id)

    # DVC tracking
    try:
        subprocess.run(["dvc", "add", output_path], check=True)
        subprocess.run(["git", "add", f"{output_path}.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", f"Track annotation for {patient_id}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] DVC tracking failed: {e}")