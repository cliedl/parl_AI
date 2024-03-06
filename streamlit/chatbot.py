import streamlit as st
from response_generator import response_generator


# Basically copied from
# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
# 2024-03-05

DELAY = 0.05  # pause between words in text stream (in seconds)

st.title("Europa Parlament - WTF?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Was willst du wissen?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator(prompt, delay=DELAY))
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
