from gtts import gTTS
import tempfile
import os

def text_to_speech(text):
    
    tts = gTTS(text=text, lang='en')

   
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)

    return temp_audio_path

