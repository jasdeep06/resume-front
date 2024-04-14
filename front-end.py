import streamlit as st
import random
import time
import requests
import os


# # Streamed response emulator
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

def make_api_call(query):
    response = requests.get("http://localhost:8000/query", params={"query": query})
    return response.json()["response"], response.json()["images"]





st.title("Simple Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"This RAG is indexed with information", "images":[]}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # st.markdown("")
        st.markdown(message["content"])
        if message["role"] == "assistant":
            for image in message["images"]:
                st.image(os.path.join("all_images",image))

# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # response = st.write_stream(response_generator())
        with st.spinner("Thinking..."):
            response,images = make_api_call(prompt)
        st.markdown(response)
        for image in images:
            st.image(os.path.join("all_images",image))

        # st.image('8351cf45-92df-4157-be3f-b6c8535bcae2-img_p1_1.png')
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "images":images})