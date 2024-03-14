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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from TTS.api import TTS
from upload_process import get_vocal_audio
from config import LANGUAGES, OUTPUTS_DIR

def agree_to_terms_of_service():
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Navigate to the terms of service page
    driver.get("https://coqui.ai/cpml.txt")

    # Automatically click the "I agree" button
    agree_button = driver.find_element_by_xpath("//button[text()='I agree']")
    agree_button.click()

    # Close the browser
    driver.quit()

def generate_cloned_voice(text, target_language, audio_file_path):
    st.write("Generating cloned voice...")

    output_file = os.path.join(OUTPUTS_DIR, "cloned_voice.wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Agree to terms of service
    agree_to_terms_of_service()

    # Proceed with TTS generation
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    try:
        vocal_audio_path = get_vocal_audio(audio_file_path)

        tts.tts_to_file(text=text, speaker_wav=vocal_audio_path, language=LANGUAGES[target_language],
                        file_path=output_file)

        st.write("Cloned voice generated successfully!")
        st.audio(output_file)

    except Exception as e:
        st.error(f"Error generating cloned voice: {e}")
