#!/bin/bash

# Start FastAPI in background on internal port (fixed, e.g. 8000)
# Redirect stdout/stderr to a log file for debugging, and run in background.
uvicorn app:app --host 0.0.0.0 --port 8000 &> uvicorn.log &
FASTAPI_PID=$! # Store the process ID of FastAPI

echo "FastAPI started with PID: $FASTAPI_PID"

# --- Health Check Loop for FastAPI ---
echo "Waiting for FastAPI to become available on port 8000..."
MAX_RETRIES=30
RETRY_DELAY=1 # seconds

for i in $(seq 1 $MAX_RETRIES); do
  # Use netcat (nc) to check if FastAPI's port is open and listening.
  # `-z` for zero-I/O (scan only), `-w 1` for a 1-second timeout.
  if nc -z -w 1 localhost 8000; then
    echo "FastAPI is up and running!"
    break # Exit the loop if FastAPI is ready
  fi
  echo "Attempt $i/$MAX_RETRIES: FastAPI not ready yet. Retrying in $RETRY_DELAY seconds..."
  sleep "$RETRY_DELAY" # Wait before the next retry

  # If max retries reached, print error and FastAPI logs, then exit.
  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "Error: FastAPI did not start in time. Check uvicorn.log for details."
    cat uvicorn.log # Print the logs of FastAPI for debugging
    exit 1 # Exit with an error code
  fi
done

# Start Streamlit on $PORT (Cloud Run routes requests here)
# `exec` replaces the current shell process with streamlit, ensuring
# signals from Docker are handled directly by Streamlit.
echo "Starting Streamlit on port $PORT..."
exec streamlit run main.py --server.port "$PORT" --server.address 0.0.0.0