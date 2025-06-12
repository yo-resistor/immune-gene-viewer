import pandas as pd
from pathlib import Path
import argparse

def annotate_variants(input_path: str, output_path: str, patient_id: str):
    """
    Annotates variants and saves output.

    Parameters:
    - input_path (str): Path to input CSV with 'Gene' and 'Allele' columns.
    - output_path (str): Final output file path.
    - patient_id (str): Patient unique ID.
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
    df["PatientID"] = patient_id

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Annotation saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    parser.add_argument("--patient_id", required=True, help="Patient ID")

    args = parser.parse_args()
    annotate_variants(args.input, args.output, args.patient_id)