import streamlit as st

st.set_page_config(
    page_title="Generate Codes",
    page_icon="📄",
    layout="wide"
)

import asyncio
import io
import os
import pathlib
from os.path import isfile, join
import pandas as pd
import helpers.sidebar
import helpers.util
import services.prompts
import services.llm
import helpers.util
from helpers import util
from services import prompts
import pyperclip

helpers.sidebar.show()

st.header("Ask Ducky for any coding help!")
st.write("Develop efficient softwares using the coding help features offered by Ducky.")

# Add a sidebar option to select the pragmatic programmer file
parent_path = pathlib.Path(__file__).parent.parent.resolve()
data_path = os.path.join(parent_path, "data")
tx_files = [f for f in os.listdir(data_path) if isfile(join(data_path, f))]
tx_dataset_name = st.sidebar.selectbox('Select a supporting document', tx_files)

# Add a sidebar option to select a help feature
feature = st.sidebar.selectbox("Select a help feature",
                                     ["Review Code", "Debug Code", "Modify Code", "Reset"])

# Create text area for user input
text_area_code = st.text_area(
    "Paste your code and specific instructions (if applicable) below and select an option from the sidebar.", value="",
    placeholder="Your code",
    height=200, key="text_area_code_editor")

# Copy Code button
if st.button("Copy Code&nbsp;&nbsp;➠", type="primary", key="copy_code_sb"):
    pyperclip.copy(text_area_code)

st.write("Your question for ducky: ")
st.code(text_area_code, language="python")

# Session state to keep track of the conversation
if "messages" not in st.session_state:
    initial_messages = [{"role": "system",
                         "content": prompts.system_learning_prompt()}]
    st.session_state.messages = initial_messages

# Mapping the selected features to its functionalities, assigning learning prompt, appending prompt to messages and start conversation.
if feature == "Review Code":
    st.title("Review Code")
    advice = st.markdown("### Code Review")
    learning_prompt = services.prompts.review_code_prompt(text_area_code)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user", "content": learning_prompt})
    st.session_state.messages = messages
    # Execute asynchronous code
    asyncio.run(helpers.util.run_conversation(messages, advice))

if feature == "Debug Code":
    st.title("Debug Code")
    advice = st.markdown("### Code Debugging")
    learning_prompt = services.prompts.debug_code_prompt(text_area_code)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user", "content": learning_prompt})
    st.session_state.messages = messages
    # Execute asynchronous code
    asyncio.run(helpers.util.run_conversation(messages, advice))

if feature == "Modify Code":
    st.title("Modify Code")
    advice = st.markdown("### Code Modification")
    learning_prompt = services.prompts.modify_code_prompt(text_area_code)

    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())

    messages.append({"role": "user", "content": learning_prompt})

    st.session_state.messages = messages
    # Execute asynchronous code
    asyncio.run(helpers.util.run_conversation(st.session_state.messages, advice))

# Clear all conversation history and start afresh with either the same code or new queries.
if feature == "Reset":
    text_area_code = st.text_area("Code", value="",
                                  placeholder="This is placeholder text when no code is present",
                                  height=200)
    st.session_state.clear()
    st.experimental_rerun()


# To allow continued conversation after clicking on features buttons.
async def chat(messages):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        messages = await util.run_conversation(messages, message_placeholder)
        st.session_state.messages = messages
    return messages


# React to the user prompt
if prompt := st.chat_input("Ask for further clarifications if needed"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    asyncio.run(chat(st.session_state.messages))
