"""
Todo list app
"""

import streamlit as st
import openai
import os

def app():

    def recipeGenerator(name_of_dish, ingredients):
        openai.organization = 'ippen'
        openai_api_key = os.environ['OPENAI_API_KEY']
        openai.api_key = openai_api_key
        headline = "Schreiben Sie ein Rezept basierend auf diesen Zutaten und Anweisungen:\n\n"
        name_of_dish = name_of_dish 
        ingredients = ingredients + "\Anweisungen:\n"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= headline + name_of_dish + ingredients,
            temperature=0.3,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)

        return response

    add_selectbox = st.sidebar.selectbox(
    "Select NLP Function?",
    ("Recipe Generator", "Summarization", "QA")
)
    if add_selectbox == "Recipe Generator":
        st.title("Test OpenAI Recipe Generator")
        name_of_dish = st.text_input("enter name of the dish", "", key="1")
        st.write('Name of the dish is', name_of_dish)
        ingredients = st.text_area("enter ingredients","", key="2")
        st.write('ingredients\n\n', ingredients)
        if st.button('Show Recipe'):
            recipe = recipeGenerator(name_of_dish, ingredients)
            st.write('eat at your own risk\n\n', recipe['choices'][0]['text'])
    else:
        st.write('coming soon...')