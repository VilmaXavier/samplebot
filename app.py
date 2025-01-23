import streamlit as st
import json

# Title and description of the app
st.set_page_config(page_title="Sample Chatbot", page_icon="🤖", layout="centered")
st.title("Sample Chatbot")

# Load JSON data
with open("college_data.json", "r") as file:
    college_data = json.load(file)

# A placeholder for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to fetch chatbot response based on user query
def get_chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Simple keyword-based matching
    if "visiting hours" in user_input or "working hours" in user_input:
        return f"Visiting hours are: {college_data['visiting_hours']['monday_to_friday']}"
    elif "contact" in user_input or "phone" in user_input:
        return f"Contact Information: Phone - {college_data['contact_information']['phone_number']}, Email - {college_data['contact_information']['email']}"
    elif "address" in user_input or "location" in user_input:
        return f"Address: {college_data['contact_information']['address']}"
    elif "notices" in user_input:
        return "Here are the latest notices:\n" + "\n".join([f"- {notice}" for notice in college_data["notices"]])
    elif "examination centre" in user_input or "exam" in user_input:
        return f"Examination Centre Email: {college_data['examination_centre']['email']}"
    else:
        return "I couldn't find the answer to that in the information I have. Please try asking something else!"

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
st.write("This is a sample chatbot application powered by DistilBERT and Streamlit.")
