import streamlit as st

import helpers.sidebar

st.set_page_config(
	page_title="Ducky",
	page_icon="🤖",
	layout="wide"
)

helpers.sidebar.show()

st.toast("Welcome to Ducky!", icon="🤖")

st.header("Welcome to ducky, your AI-powered software coding assistant!")
st.markdown("Ducky is designed to help you build efficient software applications with optimized code.")

