# audio_transcription.py
import io
import soundfile as sf
import speech_recognition as sr
import tempfile
import os
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def transcribe_audio(audio_data):
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

def generate_chatgpt_prompt(transcribed_text):
    # Use the transcribed text as a prompt for ChatGPT
    prompt = f"Transcription: {transcribed_text}\nChatGPT:"
    return prompt
