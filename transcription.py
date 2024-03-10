import os
import subprocess
import streamlit as st
import speech_recognition as sr
from config import PROCESSED_DIR


def process_audio(audio_file_path):
    st.write("Extracting audio features...")

    transcript = transcribe_audio(audio_file_path)

    return transcript


def transcribe_audio(audio_path):
    st.write("Transcribing audio...")

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(audio_data)

        st.subheader("Original Transcription")
        st.info(transcript)

        return transcript

    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return ""
