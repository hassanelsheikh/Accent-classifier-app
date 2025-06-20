FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and netcat-traditional for the health check
# `netcat-traditional` provides the `nc` command used in start.sh
RUN apt update && apt install -y ffmpeg netcat-traditional && apt clean

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Make sure the start script is executable
RUN chmod +x start.sh

# Cloud Run expects the container to listen on $PORT
EXPOSE 8080

CMD ["bash", "start.sh"]