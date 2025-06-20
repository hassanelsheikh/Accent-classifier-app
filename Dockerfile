FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and netcat-traditional for the health check
# `netcat-traditional` provides the `nc` command used in start.sh
RUN apt update && apt install -y ffmpeg netcat-traditional && apt clean

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# --- NEW STEP: Pre-download SpeechBrain Model ---
# This step loads the model once during the Docker build process.
# SpeechBrain will automatically download and cache the necessary files.
# This avoids rate-limiting issues during container startup on Cloud Run.
RUN python -c "from speechbrain.pretrained import EncoderClassifier; EncoderClassifier.from_hparams('Jzuluaga/accent-id-commonaccent_ecapa')"

# Make sure the start script is executable
RUN chmod +x start.sh

# Cloud Run expects the container to listen on $PORT
EXPOSE 8080

CMD ["bash", "start.sh"]
