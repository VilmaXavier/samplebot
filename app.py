import streamlit as st

# Title and description of the app
st.set_page_config(page_title="Sample Chatbot", page_icon="🤖", layout="centered")
st.title("Welcome to the Sample Chatbot")
st.write("Interact with the chatbot below. Ask anything!")

# Chatbot interaction
# A placeholder for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to simulate a chatbot response
def get_chatbot_response(user_input):
    # A simple response for demonstration
    responses = {
        "hello": "Hi there! How can I help you today?",
        "how are you?": "I'm just a bot, but I'm here to assist you!",
        "what is your name?": "I'm SampleBot, your virtual assistant!",
    }
    return responses.get(user_input.lower(), "I'm sorry, I didn't understand that.")

# User input form
with st.form("chat_form"):
    user_input = st.text_input("Your message:", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

# Handle form submission
if submitted and user_input:
    # Add user input to messages
    st.session_state.messages.append({"user": user_input})
    
    # Get chatbot response
    bot_response = get_chatbot_response(user_input)
    st.session_state.messages.append({"bot": bot_response})

# Display chat history
for message in st.session_state.messages:
    if "user" in message:
        st.write(f"**You:** {message['user']}")
    elif "bot" in message:
        st.write(f"**SampleBot:** {message['bot']}")

# Footer
st.write("This is a sample chatbot application created with Streamlit.")
