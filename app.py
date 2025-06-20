# app.py (FastAPI backend)
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from moviepy import VideoFileClip
from fastapi import Form
from speechbrain.pretrained import EncoderClassifier
from pathlib import Path
import requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load model once
model = EncoderClassifier.from_hparams("Jzuluaga/accent-id-commonaccent_ecapa")
labels = list(model.hparams.label_encoder.lab2ind.keys())

accent_messages = {
    "us": "🇺🇸 American accent detected — Clear, confident, and widely understood.",
    "england": "🇬🇧 British flair in your tone — Poised and articulate, ideal for formal or educational content.",
    "african": "🌍 African roots in your voice — Rich and bold, perfect for regional engagement.",
    "philippines": "🇵🇭 Filipino accent — Friendly and familiar, especially in service and support roles.",
    "canada": "🇨🇦 Canadian smoothness — Balanced and calming, a good fit for narration or e-learning.",
    "wales": "🏴 Welsh tone — Unique and lyrical, a storyteller’s choice.",
    "newzealand": "🇳🇿 Kiwi vibe — Casual and relatable, great for conversational content.",
    "singapore": "🇸🇬 Singaporean English — Crisp and bilingual-friendly, excellent for Southeast Asian audiences.",
    "indian": "🇮🇳 Indian accent — Energetic and engaging, well-suited for global tech and support.",
    "bermuda": "🏝️ Bermudian influence — Soft and rhythmic, stands out in a subtle way.",
    "ireland": "🇮🇪 Irish charm — Warm and memorable, perfect for emotional storytelling.",
    "scotland": "🏴 Scottish touch — Strong and expressive, great for passion-driven messaging.",
    "australia": "🇦🇺 Aussie accent — Friendly and confident, ideal for informal, creative projects.",
    "hongkong": "🇭🇰 Hong Kong English — Efficient and fast-paced, suited for business-oriented material.",
    "southatlandtic": "🌊 South Atlantic tone — Niche and rare, might reflect diverse linguistic influence.",
    "malaysia": "🇲🇾 Malaysian accent — Multicultural and adaptive, great for inclusive communication."
}

class AccentResult(BaseModel):
    label: str
    confidence: float
    message: str

@app.post("/analyze", response_model=AccentResult)
async def analyze_video(file: UploadFile = File(...)):
    temp_video_path = Path("uploaded_video.mp4")
    audio_path = Path("audio.wav")

    with open(temp_video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video = VideoFileClip(str(temp_video_path))
    video.audio.write_audiofile(str(audio_path))

    scores, top_score, _, predicted_label = model.classify_file(str(audio_path))

    message = accent_messages.get(predicted_label[0], "No custom message available.")

    return AccentResult(label=predicted_label[0], confidence=float(top_score), message=message)

@app.post("/analyze-url", response_model=AccentResult)
async def analyze_from_url(video_url: str = Form(...)):
    temp_video_path = Path("downloaded_video.mp4")
    audio_path = Path("audio.wav")

    # Download video file
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(temp_video_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # Extract audio
    video = VideoFileClip(str(temp_video_path))
    video.audio.write_audiofile(str(audio_path))

    # Run classification
    scores, top_score, _, predicted_label = model.classify_file(str(audio_path))
    message = accent_messages.get(predicted_label[0], "No custom message available.")

    return AccentResult(label=predicted_label[0], confidence=float(top_score), message=message)