import streamlit as st
import json
import pyttsx3
import speech_recognition as sr

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

# Speech-to-Text function
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.toast("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Load JSON data
@st.cache_data
def load_college_data():
    with open("college_data1.json", "r") as file:  # Change the filename here
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

# Main Streamlit app
def main():
    st.set_page_config(page_title="College Chatbot", page_icon="🤖", layout="centered")
    st.title("College  Chatbot")

    # Load college data
    college_data = load_college_data()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Input area with microphone
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input("Your message:", placeholder="Type or click mic to speak")
    with col2:
        mic_button = st.button("🎤")

    # Handle speech input when mic button is clicked
    if mic_button:
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
