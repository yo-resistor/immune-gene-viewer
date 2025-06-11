#!/bin/bash

# Navigate to your project directory
cd ~/immune-gene-viewer

# Activate virtual environment
source venv/bin/activate

# Pull the latest code
git pull origin main

# Kill any existing streamlit processes
pkill -f streamlit

# Optional: Reinstall dependencies (uncomment if needed)
# pip install -r requirements.txt

# Run streamlit in the background
nohup streamlit run app.py --server.port=8501 --server.headless=true > streamlit.log 2>&1 &
