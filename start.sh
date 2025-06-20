#!/bin/bash

# Use default FastAPI on $PORT if set, otherwise 8000
FASTAPI_PORT=${PORT:-8000}

# Start FastAPI in background
uvicorn app:app --host 0.0.0.0 --port $FASTAPI_PORT &

# Start Streamlit on $PORT (Cloud Run will send traffic here)
streamlit run main.py --server.port $PORT --server.address 0.0.0.0