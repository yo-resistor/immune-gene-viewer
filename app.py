import streamlit as st
import pandas as pd
import boto3
import uuid
from datetime import datetime
from pathlib import Path
from annotate import annotate_variants
import subprocess

# Optional: DynamoDB setup (toggle FALSE if not using)
USE_DYNAMODB = True
DYNAMODB_REGION = "us-west-2"
DYNAMODB_TABLE = "ImmuneGeneUploads"

if USE_DYNAMODB:
    dynamodb = boto3.resource("dynamodb", region_name=DYNAMODB_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)

st.title("🧬 Immune Gene Variant Viewer & Annotator")

# Get patient ID
patient_id = st.text_input("Enter Patient ID", value="P001")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV (columns: Gene, Allele)", type="csv")

if uploaded_file and patient_id:
    # Generate timestamped file name
    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    input_dir = Path("data/uploads")
    input_dir.mkdir(parents=True, exist_ok=True)

    # New input file name format
    input_filename = f"input_{patient_id}_{timestamp}.csv"
    input_path = input_dir / input_filename

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
        
    # Upload to S3
    s3 = boto3.client("s3")
    S3_BUCKET = "immune-viewer-dvc-bucket"
    s3_key = f"input/{input_filename}"
    s3.upload_file(str(input_path), S3_BUCKET, s3_key)
    s3_uri = f"s3://{S3_BUCKET}/{s3_key}"
    st.info(f"📤 Uploaded to S3: {s3_uri}")

    # Run annotation
    output_path = annotate_variants(str(input_path), "data/outputs", patient_id)

    # DVC track
    try:
        subprocess.run(["dvc", "add", output_path], check=True)
        subprocess.run(["git", "add", f"{output_path}.dvc"], check=True)
        subprocess.run(["git", "commit", "-m", f"Track annotation for {patient_id}"], check=True)
        st.success("📌 Output annotated and versioned with DVC.")
    except subprocess.CalledProcessError as e:
        st.error(f"❌ DVC tracking failed: {e}")

    # Display annotated data
    df = pd.read_csv(output_path)
    st.subheader("📄 Annotated Output")
    st.dataframe(df)

    # Download button
    with open(output_path, "rb") as f:
        st.download_button("Download Annotated CSV", f, file_name=Path(output_path).name)

    # Optionally log metadata to DynamoDB
    if USE_DYNAMODB:
        table.put_item(Item={
            "submission_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": patient_id,
            "input_s3_uri": s3_uri,
            "output_file_path": str(output_path),
            "output_filename": Path(output_path).name,
            "record_count": len(df)
        })
        st.info("🗃️ Metadata logged to DynamoDB.")