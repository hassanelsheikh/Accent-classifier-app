FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and dependencies
RUN apt update && apt install -y ffmpeg && apt clean

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

CMD ["bash", "start.sh"]
