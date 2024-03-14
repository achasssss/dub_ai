import os
import subprocess
import shutil
import streamlit as st
from transcription import process_audio
from translation import translate_transcription
from config import UPLOADS_DIR, PROCESSED_DIR


def process_uploaded_file(uploaded_file):
    st.write("File uploaded successfully!")

    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    audio_file_path, _ = split_audio_and_video(file_path)

    if audio_file_path:
        transcript = process_audio(audio_file_path)

        if transcript:
            translate_transcription(transcript, audio_file_path)


def split_audio_and_video(file_path):
    st.write("Splitting audio...")

    audio_path = os.path.join(PROCESSED_DIR, "audio.wav")

    if os.path.exists(audio_path):
        os.remove(audio_path)

    try:
        subprocess.run(["ffmpeg", "-y", "-i", file_path, audio_path])

        st.write("Audio split successfully!")

        return audio_path, None

    except Exception as e:
        st.error(f"Error splitting audio: {e}")
        return None, None


def get_vocal_audio(audio_file_path):
    vocal_audio_path = os.path.join(PROCESSED_DIR, "vocal_audio.wav")

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_file_path, "-ac", "1", vocal_audio_path])

        st.write("Vocal audio extracted successfully!")

        return vocal_audio_path

    except Exception as e:
        st.error(f"Error extracting vocal audio: {e}")
        return None

