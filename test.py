import streamlit as st
import io
import soundfile as sf
import speech_recognition as sr
import tempfile
import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import io
import soundfile as sf
import speech_recognition as sr
sample_rate=4410
import tempfile
import os
import numpy as np


def transcribe_audio(audio_data, sample_rate):
    recognizer = sr.Recognizer()

    with io.BytesIO(audio_data) as audio_stream:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wav_filename = temp_wav.name
            temp_wav.write(audio_data)

        # Recognize the speech from the temporary file
        audio_file = sr.AudioFile(wav_filename)
        with audio_file as source:
            audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        # Delete the temporary file
        if wav_filename:
            os.remove(wav_filename)


def main():
    st.title("Speech-to-Text with Streamlit and audio-recorder-streamlit")

    st.warning("Click the 'Record' button and start speaking to record audio.")

    # Record audio using the microphone
    audio_recording = audio_recorder()

    if audio_recording is not None:
        audio_data = audio_recording

        if st.button("Transcribe"):
            st.audio(audio_data, format="audio/wav", start_time=0)

            # Transcribe audio
            transcription = transcribe_audio(audio_data,sample_rate)
            st.write("Transcription:")
            st.write(transcription)
    else:
        st.warning("Audio recording failed. Please try again.")

if __name__ == "__main__":
    main()
