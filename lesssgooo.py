import streamlit as st
import os
import subprocess
import shutil
import speech_recognition as sr
from googletrans import Translator
import torch
from TTS.api import TTS

UPLOADS_DIR = "store/uploads"
PROCESSED_DIR = "store/processed"
OUTPUTS_DIR = "store/outputs"
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Hindi": "hi",
}


def main():
    st.set_page_config(layout="wide")  # Set layout to wide to cover the entire screen
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            justify-content: center;
        }
        .big-bold-text {
            font-size: 56px;
            font-weight: bold;
        }
        </style>
        """
        , unsafe_allow_html=True)
    st.markdown('<p class="centered big-bold-text">dub AI</p>', unsafe_allow_html=True)

    # Notes and audio files on the left side
    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown("### Notes:")
        st.markdown("- Transcription and translation accuracy need significant improvement.")
        st.markdown("- The voice cloning model has limitations regarding the number of words it can produce.")
        st.markdown("- The current version is intended for reference only and is undergoing substantial enhancements.")
        st.markdown("##### Here's the best generated audio alongside the original for comparison.")

        sample_folder = "sample"
        audio_files = [f for f in os.listdir(sample_folder) if f.endswith(".wav")]

        if len(audio_files) == 0:
            st.write("No audio files found in the 'sample' folder.")
        else:
            # Sort the audio files based on the numeric part of the filename
            audio_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

            for file_name in audio_files:
                file_title = file_name.replace(".wav", "")
                st.write(f"{file_title}")
                file_path = os.path.join(sample_folder, file_name)
                st.audio(file_path, format='audio/wav')

    with right_column:
        st.markdown("### Upload Here")

        # Step 1: Upload file
        uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav", "mp4", "mov"])

        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)


def process_uploaded_file(uploaded_file):
    # Save the uploaded file
    file_path = save_uploaded_file(uploaded_file)

    if file_path:
        # Step 2: Extract audio and video
        audio_file_path, _ = split_audio_and_video(file_path)

        if audio_file_path:
            # Step 3: Extract audio features
            transcript = extract_audio_features(audio_file_path)

            if transcript:
                # Step 4: Transcribe vocal audio and translate
                translate_transcription(transcript, audio_file_path)


def save_uploaded_file(uploaded_file):
    st.write("File uploaded successfully!")

    # Save the uploaded file
    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def split_audio_and_video(file_path):
    st.write("Splitting audio...")

    # Define paths for output files
    audio_path = os.path.join(PROCESSED_DIR, "audio.wav")

    # Remove existing files if present
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Use FFmpeg to split audio
    try:
        # Convert video to audio
        subprocess.run(["ffmpeg", "-y", "-i", file_path, audio_path])  # Added "-y" for default overwrite

        st.write("Audio split successfully!")

        return audio_path, None

    except Exception as e:
        st.error(f"Error splitting audio: {e}")
        return None, None


def extract_audio_features(audio_file_path):
    st.write("Extracting audio features...")

    # Transcribe vocal audio
    transcript = transcribe_audio(audio_file_path)

    return transcript


def transcribe_audio(audio_path):
    st.write("Transcribing audio...")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    try:
        # Load audio file
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Record audio data from file
            audio_data = recognizer.record(source)

        # Transcribe speech using Google Web Speech API
        transcript = recognizer.recognize_google(audio_data)

        # Display the transcription in a box
        st.subheader("Original Transcription")
        st.info(transcript)

        return transcript

    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return ""


def translate_transcription(transcript, audio_file_path):
    st.write("Translating transcription...")

    # Choose target language
    target_language = st.selectbox("Select Target Language", list(LANGUAGES.keys()))

    # Display translation button
    if st.button("Lesss gooo"):
        # Initialize translator
        translator = Translator()

        try:
            # Translate transcription to the target language
            translated_text = translator.translate(transcript, dest=LANGUAGES[target_language]).text

            # Display the translated text
            st.subheader("Translated Transcription")
            st.info(translated_text)

            # Step 5: Generate cloned voice for translated text
            generate_cloned_voice(translated_text, target_language, audio_file_path)

        except Exception as e:
            st.error(f"Error translating transcription: {e}")


def generate_cloned_voice(text, target_language, audio_file_path):
    st.write("Generating cloned voice...")

    # Construct the output file path
    output_file = os.path.join(OUTPUTS_DIR, "cloned_voice.wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    try:
        # Get vocal part of the audio
        vocal_audio_path = get_vocal_audio(audio_file_path)

        # Generate cloned voice using vocal audio
        tts.tts_to_file(text=text, speaker_wav=vocal_audio_path, language=LANGUAGES[target_language],
                        file_path=output_file)

        st.write("Cloned voice generated successfully!")

        # Display the output audio
        st.audio(output_file)

    except Exception as e:
        st.error(f"Error generating cloned voice: {e}")


def get_vocal_audio(audio_file_path):
    # Define path for output vocal file
    vocal_audio_path = os.path.join(PROCESSED_DIR, "vocal_audio.wav")

    # Use FFmpeg to extract vocal part of the audio
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_file_path, "-ac", "1", vocal_audio_path])  # Added "-y" for default overwrite

        st.write("Vocal audio extracted successfully!")

        return vocal_audio_path

    except Exception as e:
        st.error(f"Error extracting vocal audio: {e}")
        return None


if __name__ == "__main__":
    main()
