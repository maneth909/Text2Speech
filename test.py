import streamlit as st
from gtts import gTTS  # Google Text-to-Speech
from io import BytesIO  # in-memory binary streams, handling audio data without writing it to disk.
from pydub import AudioSegment  # manipulating audio files.
import tempfile
import os

# Function to convert text to speech
def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language, slow=False)  # False normal speech speed.
        return tts
    except Exception as e:
        st.error(f"Error in text-to-speech conversion: {e}")
        return None

# Function to play audio
def play_audio(audio_file):
    try:
        audio_file.seek(0)  # Point to the beginning of the file.
        audio = AudioSegment.from_file(audio_file, format="mp3")  # Create AudioSegment from the file-like object.
        play(audio)
    except Exception as e:
        st.error(f"Error in playing audio: {e}")

def change_playback_speed(audio, speed=1.0):
    new_frame_rate = int(audio.frame_rate * speed)
    return audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate}).set_frame_rate(audio.frame_rate)

# Streamlit interface
st.title("Text to Speech Conversion")
st.write("Enter the text you want to convert to speech")

# Text input
user_text = st.text_area("Type your text here")

# Language selection
language = st.selectbox("Select language", ['en', 'es', 'fr', 'de', 'zh-TW', 'zh-CN', 'pt'])

speech_speed = st.sidebar.slider("Adjust speed", 0.5, 2.0, 1.0, step=0.1)

if st.button("Convert to Speech"):
    if user_text:
        tts = text_to_speech(user_text, language)
        if tts:
            audio_file = BytesIO()
            try:
                tts.write_to_fp(audio_file)  # write the audio
                audio_file.seek(0)
                
                # Save the audio file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    tts.save(temp_file.name)
                    st.audio(temp_file.name, format='audio/mp3')

                    adjusted_audio = change_playback_speed(audio, speech_speed)
                    
                    # Save the adjusted audio to a new temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as adjusted_temp_file:
                        adjusted_audio.export(adjusted_temp_file.name, format="mp3")
                        st.audio(adjusted_temp_file.name, format='audio/mp3')
                    
                    os.remove(temp_file.name)
                    os.remove(adjusted_temp_file.name)

            except Exception as e:
                st.error(f"Error in writing or handling audio file: {e}")
    else:
        st.warning("Please enter some text to convert to speech.")