#!/bin/bash

# Start FastAPI in background on internal port (fixed, e.g. 8000)
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on $PORT (Cloud Run routes requests here)
streamlit run main.py --server.port $PORT --server.address 0.0.0.0
