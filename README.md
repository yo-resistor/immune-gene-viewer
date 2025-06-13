# 🧬 Immune Gene Variant Viewer & Annotator
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yo-resistor/immune-gene-viewer/blob/main/LICENSE)

A lightweight web application to **upload, annotate, and view immune-related gene variants**. Designed as a toy project to demonstrate an end-to-end data annotation pipeline with reproducibility, AWS integration, and Streamlit deployment.

## 🧪 Try the Live Demo

You can test the web app live here:  
🌐 [http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501/](http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501/)

### 📜 Test Instructions

1. Go to the app link above
2. In the **Patient ID** field, enter: `PTEST` 
3. Upload a CSV file with the following content:

 ```csv
 Gene,Allele
 HLA-B,B*08:01
 HLA-B,B*15:01
 HLA-A,A*02:01
 ```

 Or 📄 [download Sample Input CSV](https://github.com/yo-resistor/immune-gene-viewer/blob/main/sample_input.csv) here.

4. View your annotated results directly on the page
5. The run will be logged and versioned behind the scenes using DVC and DynamoDB
6. The input and output data will be stored in S3 using SSE (Server Side Encryption)

💡 *You can try entering different Patient IDs (e.g., P001, P002) or change allele inputs to see how the risk classification adapts.*

## 🧠 Purpose

The project was built as a toy prototype to demonstrate:
- Streamlit frontend + cloud backend integration
- DVC-powered reproducibility
- Lightweight bioinformatics tools for clinical/biotech applications

## 🚀 Features

- Upload CSV files containing immune gene variants (format: `Gene`, `Allele`)
- Run annotation logic and generate risk assessments
- View and download annotated results
- Logs and tracks annotated runs using a local `logs.csv`
- AWS-Ready:
  - Hosted on EC2
  - Input/output logging with **DynamoDB**
  - S3-based **data versioning** with DVC
- Simulates secure handling of sensitive data using encryption and IAM scoping

## 📦 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: AWS DynamoDB  
- **Storage & Versioning**: AWS S3 + DVC  
- **Deployment**: EC2 (Ubuntu), `tmux` for persistent sessions  
- **Pipeline Logging**: `dvc.yaml` + custom DVC stages

## 🏛️ Architecture Overview
```
                +-----------------------+
                |   User (Web Client)   |
                +-----------+-----------+
                            |
                            v
              +-------------+-------------+
              |   EC2 Instance (Ubuntu)   |
              |   - Hosts Streamlit app   |
              |   - Uses tmux to persist  |
              +-------------+-------------+
                            |
            +---------------+---------------+
            |                               |
            v                               v
+-----------+-----------+       +-----------+------------+
|   AWS S3              |       |   AWS DynamoDB         |
|   - Upload storage    |       |   - Logs Patient ID,   |
|   - DVC versioning    |       |     input time, etc.   |
+-----------------------+       +------------------------+
```

## 🧑‍💻 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yo-resistor/immune-gene-viewer.git
cd immune-gene-viewer
```

### 2. Set up the environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure AWS credentials

Set up your AWS credentials (via `~/.aws/credentials` or environment variables).

### 4. Run locally

```bash
streamlit run app.py
```
or 
```bash
bash scripts/deploy.sh
```

## 🧪 Annotation Logic

The core logic uses a simple risk scoring system based on allele types:
```python
def risk_logic(allele):
    if "B*08" in allele:
        return "Very High"
    elif "B" in allele:
        return "High"
    elif "A" in allele:
        return "Moderate"
    else:
        return "Low"
```

## 📁 File Structure

```
data/
├── uploads/       # uploaded input CSVs
├── outputs/       # annotated results
└── logs.csv       # log of all runs
app.py             # Streamlit UI
annotate.py        # annotation logic
dvc_utils.py       # DVC integration
run_annotation.py  # standalone CLI annotation with DVC tracking
```

## 📘 Future Work

- Add variant-disease mapping using public APIs
- Improve the annotation logic
- Full HTTPS setup with domain
- User authentication and role-based access
- CI/CD with GitHub Actions
- Containerization using ECS or EKS

## 📜 License

MIT License

Copyright (c) 2025 Yunsik Ohm
