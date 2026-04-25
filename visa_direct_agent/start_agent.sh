#!/bin/bash

# Navigate to the correct directory (just in case)
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# Run the streamlit app
streamlit run app.py
