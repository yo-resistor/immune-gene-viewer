import streamlit as st
import pandas as pd
import boto3
import json
import uuid
from datetime import datetime

# Load annotation map
with open("annotation_map.json") as f:
    annotations = json.load(f)

# Setup DynamoDB (region might be different depending on your table)
dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
table = dynamodb.Table("ImmuneGeneUploads")

st.title("Immune Gene Variant Viewer & Annotator")

uploaded_file = st.file_uploader("Upload your CSV (columns: Gene, Allele)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []

    for _, row in df.iterrows():
        gene = row["Gene"]
        allele = row["Allele"]
        note = annotations.get(allele, "No annotation available")

        entry = {
            "Gene": gene,
            "Allele": allele,
            "Annotation": note
        }

        # Write to DynamoDB
        table.put_item(Item={
            "submission_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "Gene": gene,
            "Allele": allele,
            "Annotation": note
        })

        results.append(entry)

    st.success("File processed successfully.")
    st.dataframe(pd.DataFrame(results))