FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and netcat-traditional for health checks
RUN apt update && apt install -y ffmpeg netcat-traditional && apt clean

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Pre-download SpeechBrain model ---
RUN python -c "\
from speechbrain.inference.speaker import EncoderClassifier; \
EncoderClassifier.from_hparams(source='Jzuluaga/accent-id-commonaccent_ecapa', \
save_folder='/app/sb_models/accent-model')"


# Copy cached model into app directory to persist it
RUN mkdir -p /app/sb_models && cp -r /root/.cache/speechbrain/* /app/sb_models/

# Make the start script executable
RUN chmod +x start.sh

# Cloud Run expects the container to listen on $PORT
EXPOSE 8080

# Start both FastAPI and Streamlit
CMD ["bash", "start.sh"]
