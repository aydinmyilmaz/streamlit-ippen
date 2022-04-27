"""
Todo list app
"""

import streamlit as st
import openai
import os
import json

def app():

    def recipeGenerator(name_of_dish, ingredients):
        openai.organization = 'ippen'
        openai_api_key = os.environ.get('OPENAI_API_KEY')
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

    def summary(text):
        openai.organization = 'ippen'
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        openai.api_key = openai_api_key
        text = text + "\n\nTl;dr"
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        return response['choices'][0]['text']


    add_selectbox = st.sidebar.selectbox(
    "Select NLP Function?",
    ("Recipe Generator", "Summarization", "QA")
)
    if add_selectbox == "Recipe Generator":
        st.title("OpenAI Recipe Generator")
        name_of_dish = st.text_input("Enter name of the dish", "", key="1")
        st.write('Name of the dish is', name_of_dish)
        ingredients = st.text_area("Enter ingredients","", key="2")
        st.markdown('**ingredients**\n\n', ingredients)
        if st.button('Show Recipe'):
            recipe = recipeGenerator(name_of_dish, ingredients)
            st.markdown('**eat at your own risk!!!**\n\n', recipe['choices'][0]['text'])
    
    elif add_selectbox == "Summarization":
        st.title("OpenAI Summarization")
        
        # path = "data_1000.json"
        # with open(path, 'r') as json_file:
        #     data = json.load(json_file)
        # st.sidebar.title('Selection Menu')
        # st.sidebar.header('Select Parameters')
        # idx = str(st.sidebar.number_input('Insert an index number between 0-1000 to select a random Story', min_value=0, max_value=10000, value=0))
        # st.write('**Online Id:**', data[idx]['meta']['online_id'])
        # text = data[idx]['meta']['text'][0:500]
        
        text = st.text_area("Enter a text in german to summarize","", key="1")
        st.write('**Text:**', text[0:500])
        res_summary = summary(text[0:500])
        if st.button('Show Summary'):
            st.write('**Summary:**', res_summary)

    else:
        st.write('coming soon...')
