#!/bin/bash

# Use PORT from environment (default to 8080)
PORT=${PORT:-8080}

# Start FastAPI in background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on Cloud Run expected port
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
