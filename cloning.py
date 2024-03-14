# import os
# import streamlit as st
# import torch
# from TTS.api import TTS
# from upload_process import get_vocal_audio
# from config import LANGUAGES, OUTPUTS_DIR

# def generate_cloned_voice(text, target_language, audio_file_path):
#     st.write("Generating cloned voice...")

#     output_file = os.path.join(OUTPUTS_DIR, "cloned_voice.wav")

#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

#     try:
#         vocal_audio_path = get_vocal_audio(audio_file_path)

#         tts.tts_to_file(text=text, speaker_wav=vocal_audio_path, language=LANGUAGES[target_language],
#                         file_path=output_file)

#         st.write("Cloned voice generated successfully!")
#         st.audio(output_file)

#     except Exception as e:
#         st.error(f"Error generating cloned voice: {e}")


import os
import streamlit as st
import torch
from TTS.api import TTS
from upload_process import get_vocal_audio
from config import LANGUAGES, OUTPUTS_DIR

def generate_cloned_voice(text, target_language, audio_file_path):
    st.write("Generating cloned voice...")

    output_file = os.path.join(OUTPUTS_DIR, "cloned_voice.wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if st.button("Accept Terms of Service"):
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        try:
            vocal_audio_path = get_vocal_audio(audio_file_path)

            tts.tts_to_file(text=text, speaker_wav=vocal_audio_path, language=LANGUAGES[target_language],
                            file_path=output_file)

            st.write("Cloned voice generated successfully!")
            st.audio(output_file)

        except Exception as e:
            st.error(f"Error generating cloned voice: {e}")
    else:
        st.warning("You must accept the terms of service to use this model.")

