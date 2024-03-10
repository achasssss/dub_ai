import streamlit as st
from googletrans import Translator
from config import LANGUAGES


def translate_transcription(transcript, audio_file_path):
    from cloning import generate_cloned_voice  # Import inside the function to avoid circular import

    st.write("Translating transcription...")

    target_language = st.selectbox("Select Target Language", list(LANGUAGES.keys()))

    if st.button("Lesss gooo"):
        translator = Translator()

        try:
            translated_text = translator.translate(transcript, dest=LANGUAGES[target_language]).text

            st.subheader("Translated Transcription")
            st.info(translated_text)

            generate_cloned_voice(translated_text, target_language, audio_file_path)

        except Exception as e:
            st.error(f"Error translating transcription: {e}")
