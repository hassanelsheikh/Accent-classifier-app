import streamlit as st
import requests
import os

st.set_page_config(page_title="Accent Identifier", layout="centered")
st.title("🗣️ English Accent Identifier")
st.write("Upload a short MP4 video or paste a direct video URL to detect the speaker's accent")

# --- Upload video from local file ---
uploaded_file = st.file_uploader("📁 Upload your video (MP4)", type=["mp4"])

# --- OR paste a URL ---
st.markdown("### 🔗 Or paste a direct MP4 video URL")
video_url = st.text_input("Paste a direct .mp4 URL here")

st.markdown("### Or try an example:")
#Add placeholder for example video selection
example = st.selectbox(
    "Select an example video",
    options=[""] + [f for f in os.listdir("examples") if f.endswith(".mp4")],
    index=0
)

# Process file upload
if uploaded_file is not None:
    with st.spinner("Processing uploaded video..."):
        # Save locally
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        # Send to FastAPI
        files = {"file": open(video_path, "rb")}
        response = requests.post("http://localhost:8000/analyze", files=files)

        if response.status_code == 200:
            result = response.json()
            st.success("Accent detected!")
            st.markdown(f"### 🏷️ **Predicted Accent:** `{result['label'].capitalize()}`")
            st.markdown(f"**Confidence:** `{result['confidence'] * 100:.2f}%`")
            st.info(result['message'])

            if "all_scores" in result:
                st.markdown("---")
                st.markdown("#### 🔢 All Accent Scores:")
                for accent, score in result["all_scores"]:
                    st.write(f"{accent:15}: {score * 100:.2f}%")
        else:
            st.error("Failed to process the uploaded video.")

# Process URL input
elif video_url:
    with st.spinner("Fetching video from URL..."):
        response = requests.post("http://localhost:8000/analyze-url", data={"video_url": video_url})

        if response.status_code == 200:
            result = response.json()
            st.success("Accent detected from URL!")
            st.markdown(f"### 🏷️ **Predicted Accent:** `{result['label'].capitalize()}`")
            st.markdown(f"**Confidence:** `{result['confidence'] * 100:.2f}%`")
            st.info(result['message'])

            if "all_scores" in result:
                st.markdown("---")
                st.markdown("#### All Accent Scores:")
                for accent, score in result["all_scores"]:
                    st.write(f"{accent:15}: {score * 100:.2f}%")
        else:
            st.error("Failed to process the video URL.")
# Process example video selection
elif example:
    example_path = os.path.join("examples", example)

    if os.path.exists(example_path):
        with st.spinner(f"Processing example: {example}..."):
            files = {"file": open(example_path, "rb")}
            response = requests.post("http://localhost:8000/analyze", files=files)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Accent detected from example: `{example}`")
                st.markdown(f"### 🏷️ **Predicted Accent:** `{result['label'].capitalize()}`")
                st.markdown(f"**Confidence:** `{result['confidence'] * 100:.2f}%`")
                st.info(result['message'])

                if "all_scores" in result:
                    st.markdown("---")
                    st.markdown("#### 🔢 All Accent Scores:")
                    for accent, score in result["all_scores"]:
                        st.write(f"{accent:15}: {score * 100:.2f}%")
            else:
                st.error(f"Failed to process example: {example}")
    else:
        st.error(f"⚠️ File not found: {example_path}")