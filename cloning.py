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

def agree_to_terms_of_service():
    st.markdown("## Terms of Service")
    st.write("This license allows only non-commercial use of a machine learning model and its outputs.")
    agreement = st.checkbox("I have read, understood, and agreed to the Terms and Conditions.")
    return agreement

def generate_cloned_voice(text, target_language, audio_file_path):
    st.write("Generating cloned voice...")

    output_file = os.path.join(OUTPUTS_DIR, "cloned_voice.wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Agree to terms of service
    if agree_to_terms_of_service():
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
        st.warning("Failed to agree to the terms of service. Cloned voice generation aborted.")
