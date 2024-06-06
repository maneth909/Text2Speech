import streamlit as st
from gtts import gTTS 
from io import BytesIO 
from pydub import AudioSegment 
import tempfile
import os

language_code = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Portuguese': 'pt',
    'Chinese (Mandarin)': 'zh-CN',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Dutch': 'nl',
    'Russian': 'ru',
    'Hindi': 'hi',
    'Arabic': 'ar'
}

# Function to convert text to speech
def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language, slow=False) 
        return tts
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to change the speed
def adjust_speed(audio, speed=1.0):
    new_frame_rate = int(audio.frame_rate * speed)
    adjusted = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
    return adjusted.set_frame_rate(audio.frame_rate)


st.title("Text to Speech Conversion")

col1, col2 = st.columns([2, 1])
with col1:
    user_text = st.text_area("Type your text here")

with col2:
    language = st.selectbox("Select language", language_code)
    if st.button("Convert to Speech"):
        convert_to_speech = True
    else:
        convert_to_speech = False

speech_speed = st.sidebar.slider("Adjust speed", 0.5, 2.0, 1.0, step=0.1)

if convert_to_speech:
    if user_text:
        tts = text_to_speech(user_text, language_code[language])
        if tts:
            audio_file = BytesIO()
            try:
                tts.write_to_fp(audio_file) 
                audio_file.seek(0)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    tts.save(temp_file.name)
                    audio = AudioSegment.from_file(temp_file.name, format="mp3")
                    
                    adjusted = adjust_speed(audio, speech_speed)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as adjusted_temp_file:
                        adjusted.export(adjusted_temp_file.name, format="mp3")

                        st.write("### Input Text:")
                        st.write(user_text)

                        st.audio(adjusted_temp_file.name, format='audio/mp3')
                    
                    os.remove(temp_file.name)
                    os.remove(adjusted_temp_file.name)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text.")