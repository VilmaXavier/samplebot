import streamlit as st
import json
import pyttsx3
import speech_recognition as sr
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

# Initialize TTS engine
def init_tts_engine():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        return engine
    except Exception as e:
        st.error(f"TTS init error: {e}")
        return None

# Speak text function
def speak_text(text):
    try:
        tts_engine = init_tts_engine()
        if tts_engine:
            tts_engine.say(text)
            tts_engine.runAndWait()
    except Exception as e:
        st.error(f"Speech error: {e}")

# Load JSON data
@st.cache_data
def load_college_data():
    with open("college_data1.json", "r") as file:
        return json.load(file)

# Chatbot response function
def get_chatbot_response(user_input, college_data):
    user_input = user_input.lower()
    
    response_map = {
        "notices": "Latest notices:\n" + "\n".join([f"- {notice}" for notice in college_data["paragraphs"]]),
        "links": "You can find more information at these links:\n" + "\n".join([f"- {link}" for link in college_data["links"]]),
    }
    
    for key, response in response_map.items():
        if key in user_input:
            return response
    
    return "I couldn't find an answer. Please rephrase."

# WebRTC Audio Processor for Speech-to-Text
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = np.array(frame.to_ndarray())  # Convert audio frame to NumPy array
        
        # Convert audio to speech_recognition-compatible format
        audio_data = sr.AudioData(audio.tobytes(), frame.sample_rate, 2)
        
        try:
            text = self.recognizer.recognize_google(audio_data)
            st.session_state["transcribed_text"] = text
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition API error: {e}")

        return frame  # Return unchanged audio frame

# Speech-to-Text function using WebRTC
def speech_to_text():
    webrtc_streamer(key="speech", mode=WebRtcMode.SENDRECV, audio_processor_factory=AudioProcessor)

    # Display transcribed text
    if "transcribed_text" in st.session_state:
        return st.session_state["transcribed_text"]
    return ""

# Main Streamlit app
def main():
    st.set_page_config(page_title="College Chatbot", page_icon="🤖", layout="centered")
    st.title("College Chatbot with Speech Recognition")

    # Load college data
    college_data = load_college_data()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # UI: Text input with microphone button
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input("Your message:", placeholder="Type or click mic to speak")
    with col2:
        mic_button = st.button("🎤")

    # Handle speech input when mic button is clicked
    if mic_button:
        st.subheader("🎤 Speak now:")
        user_input = speech_to_text()

    # Process input if user input is available
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response and add it to chat history
        bot_response = get_chatbot_response(user_input, college_data)
        st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Display chat history and read aloud buttons
    for idx, message in enumerate(st.session_state.messages):
        if message['role'] == 'user':
            st.write(f"**You:** {message['content']}")
        else:
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.write(f"**SampleBot:** {message['content']}")
            with col2:
                # Unique key for each speak button
                if st.button("🔊", key=f"speak_{idx}"):
                    speak_text(message['content'])

if __name__ == "__main__":
    main()
