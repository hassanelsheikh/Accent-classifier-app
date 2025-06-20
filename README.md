

```markdown
# 🗣️ English Accent Identifier
Try it now
https://accentclassifier-955024163421.europe-west1.run.app/


This project allows users to upload or link to a short `.mp4` video containing spoken English, and it detects the speaker's **accent** using a pre-trained SpeechBrain model.

Built with:
- **FastAPI** (for backend inference)
- **Streamlit** (for frontend user interface)
- **SpeechBrain** (for accent classification)

---

## 🔧 Features

- Upload local `.mp4` videos or paste a direct video URL
- Example videos included for quick testing
- Real-time accent classification with confidence scores
- Friendly messages tailored to each accent

---

## 📁 Project Structure

```

accent-identifier/
├── app.py                 # FastAPI backend
├── streamlit\_app.py       # Streamlit frontend
├── examples/              # Folder with sample MP4 videos
├── Dockerfile             # Unified container with FastAPI + Streamlit
├── requirements.txt
├── start.sh               # Bash script to run both servers
└── README.md

````

---

## ⚙️ Local Setup (Linux/macOS/WSL)

### 1. Clone the repo

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run backend and frontend

```bash
# Run FastAPI
uvicorn app:app --reload --port 8000

# In a new terminal
streamlit run streamlit_app.py --server.port 8501
```

Open [http://localhost:8501](http://localhost:8501) to try it out.

---

## 🐳 Dockerized Deployment

### 1. Build & run locally

```bash
docker build -t accent-identifier .
docker run -p 8000:8000 -p 8501:8501 accent-identifier
```

### 2. Access:

* FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Streamlit: [http://localhost:8501](http://localhost:8501)

---

## ☁️ GCP Deployment (Compute Engine or Cloud Run)

### Option A: GCP Compute Engine

1. Create a VM (Ubuntu + Docker)
2. Upload the repo and run:

```bash
bash start.sh
```

Make sure ports `8000` and `8501` are open in your firewall rules.

### Option B: GCP Cloud Run

To deploy with Cloud Run (Streamlit-only or nginx-combined):

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/accent-identifier
gcloud run deploy accent-identifier \
  --image gcr.io/YOUR_PROJECT_ID/accent-identifier \
  --platform managed \
  --allow-unauthenticated \
  --port 8501
```

---

## 📦 Requirements

* Python 3.9+
* `ffmpeg` installed (used by `moviepy`)
* GPU optional (CPU works fine for small clips)

---

## 📌 Notes

* Use short clips (5–20 seconds) for best results
* The SpeechBrain model used: `Jzuluaga/accent-id-commonaccent_ecapa`
* Temporary files are handled using `tempfile.TemporaryDirectory` internally

---

## 🤝 License

MIT License. Feel free to fork and modify!

```


