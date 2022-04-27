
import streamlit as st

# Custom imports 
from multipage import MultiPage
import ner
import tts
import appopenai
import huggface
from PIL import Image

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Ippen Digital - NLP Lab")
image = Image.open('nlp.jpeg')
st.image(image)

# Add all your applications (pages) here
app.add_page("Named Entity Recognition", ner.app)
app.add_page("Text-2-Speech", tts.app)
app.add_page("OpenAI GPT-3", appopenai.app)
app.add_page("Open Source GPT-2", huggface.app)
# The main app
app.run()