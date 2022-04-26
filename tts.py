import streamlit as st
import json 
from IPython.display import display, HTML, Audio
from gtts import gTTS
import streamlit.components.v1 as components
from boto3 import client



def app():

    path = "data_1000.json"
    with open(path, 'r') as json_file:
        data = json.load(json_file)

    st.sidebar.title('Selection Menu')
    st.sidebar.header('Select Parameters')

    idx = str(st.sidebar.number_input('Insert an index number between 0-1000 to select a random Story', min_value=0, max_value=10000, value=0))
    text = data[idx]['meta']['text']
    st.write('Article:\n', text)

    def text_2_speech(text):
        tts = gTTS(text[0:500], lang="de", slow=False)
        tts.save("1.wav")
        sound_file = open('1.wav','rb')
        audio_bytes = sound_file.read()
        return st.audio(audio_bytes, format='audio/ogg')

    def googlepolly_tts(text, voice):
        polly = client('polly', region_name='us-west-2')
        response = polly.synthesize_speech(
                Text=text[0:500],
                OutputFormat='mp3',
                VoiceId=voice)
        stream = response.get('AudioStream')
        with open('output_aws_polly.mp3', 'wb') as f:
            data = stream.read()
            f.write(data)
        sound_file = open('output_aws_polly.mp3','rb')
        audio_bytes = sound_file.read()
        return st.audio(audio_bytes, format='audio/ogg')


    st.sidebar.header('Select Parameter and Function for Voice')

    voice = st.sidebar.selectbox('Select voice', ['Amelie'])
    if st.sidebar.button(f'Run open source Text-2-Speech'):
        text = data[idx]['meta']['text']
        text_2_speech(text)

    voice = st.sidebar.selectbox('Select voice', ['Vicki', 'Marlene','Hans'])
    if st.sidebar.button(f'Run AWS Polly Text-2-Speech'): 
        text = data[idx]['meta']['text']
        googlepolly_tts(text, voice)

