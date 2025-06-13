# 🧬 Immune Gene Variant Viewer & Annotator
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yo-resistor/immune-gene-viewer/blob/main/LICENSE)

A lightweight web application to **upload, annotate, and view immune-related gene variants**. Designed as a toy project to demonstrate an end-to-end data annotation pipeline with reproducibility, AWS integration, and Streamlit deployment.

🌐 Live Demo: [http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501](http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501)

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

---

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

---

## 📁 File Structure

```
data/
├── uploads/       # uploaded input CSVs
├── outputs/       # annotated results
├── logs.csv       # log of all runs
app.py             # Streamlit UI
annotate.py        # annotation logic
dvc_utils.py       # DVC integration
run_annotation.py  # standalone CLI annotation with DVC tracking
```

---

## 📘 Future Work

- Add variant-disease mapping using public APIs
- Improve the annotation logic
- Full HTTPS setup with domain
- User authentication and role-based access
- CI/CD with GitHub Actions
- Containerization using ECS or EKS

---

## 📜 License
MIT License

Copyright (c) 2025 Yunsik Ohm
