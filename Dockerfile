FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and netcat-traditional for health checks
RUN apt update && apt install -y ffmpeg netcat-traditional && apt clean

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the start script executable
RUN chmod +x start.sh

# Expose port for Streamlit (Cloud Run expects $PORT)
EXPOSE 8080

# Start FastAPI and Streamlit
CMD ["bash", "start.sh"]
