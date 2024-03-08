# main_app.py
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from transcribe import transcribe_audio
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import io
import base64
import re
from langchain_core.output_parsers import StrOutputParser
import tempfile
import os
from TTS import text_to_speech
from dotenv import load_dotenv




def main():
    st.title("STT-GPT-TTS")

    st.warning("Click the 'Record' button and start speaking to record audio.")

    
    audio_recording = audio_recorder()

    if audio_recording is not None:
        audio_data = audio_recording

        if st.button("Generate"):
            

            # Transcribe audio
            transcription = transcribe_audio(audio_data)
            st.write("prompt:")
            st.write(transcription)

            # Feed transcribed text to ChatGPT
            chatgpt_input = f"Transcription: {transcription}\nChatGPT:"
            
            load_dotenv()
            openai_key = os.getenv("OPENAI_API_KEY")
            llm = ChatOpenAI(openai_api_key=openai_key)
            response = llm.invoke(chatgpt_input)
            
            st.write("ChatGPT Response:")
            output_parser=StrOutputParser()
            string=output_parser.invoke(response)
            st.write(string)
            
            tts_audio = text_to_speech(string)
            st.audio(tts_audio, format="audio/mpeg", start_time=0)
    else:
        st.warning("Please try again.")

if __name__ == "__main__":
    main()


