# 🧬 Immune Gene Variant Viewer & Annotator

A lightweight web application to **upload, annotate, and view immune-related gene variants**. Designed as a toy project to demonstrate an end-to-end data annotation pipeline with reproducibility, AWS integration, and Streamlit deployment.

🌐 Live Demo: [http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501](http://ec2-52-42-31-181.us-west-2.compute.amazonaws.com:8501)

---

## 🚀 Features

- 🔬 Upload CSV files containing immune gene variants (format: `Gene`, `Allele`)
- ⚙️ Run annotation logic and generate risk assessments
- 📝 View and download annotated results
- 🔁 Logs and tracks annotated runs using a local `logs.csv`
- ☁️ AWS-Ready:
  - Hosted on EC2
  - Input/output logging with **DynamoDB**
  - S3-based **data versioning** with DVC
- 🔐 Simulates secure handling of sensitive data using encryption and IAM scoping

---

## 📦 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: AWS DynamoDB  
- **Storage & Versioning**: AWS S3 + DVC  
- **Deployment**: EC2 (Ubuntu), `tmux` for persistent sessions  
- **Pipeline Logging**: `dvc.yaml` + custom DVC stages

---

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
