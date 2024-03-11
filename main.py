import os
import streamlit as st
from transcription import process_audio
from translation import translate_transcription
from upload_process import process_uploaded_file


def main():
    st.set_page_config(layout="wide")
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
            audio_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

            for file_name in audio_files:
                file_title = file_name.replace(".wav", "")
                st.write(f"{file_title}")
                file_path = os.path.join(sample_folder, file_name)
                st.audio(file_path, format='audio/wav')

    with right_column:
        st.markdown("### Upload Here")

        uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav", "mp4", "mov"])

        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)


if __name__ == "__main__":
    main()
