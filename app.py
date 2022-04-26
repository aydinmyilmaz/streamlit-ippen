
import streamlit as st

# Custom imports 
from multipage import MultiPage
import ner
import tts
import appopenai

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Ippen Digital - NLP Applications")

# Add all your applications (pages) here
app.add_page("Named Entity Recognition", ner.app)
app.add_page("Text-2-Speech", tts.app)
app.add_page("OpenAI GPT-3", appopenai.app)
# The main app
app.run()