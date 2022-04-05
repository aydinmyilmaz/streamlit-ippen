import streamlit as st
import json 
from IPython.display import display, HTML, Audio
from gtts import gTTS
import style_utils as style_config
import streamlit.components.v1 as components
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from boto3 import client
st.set_page_config(layout="wide")

st.title('Analyse NER')

path = "data_1000.json"

with open(path, 'r') as json_file:
    data = json.load(json_file)

st.sidebar.title('Selection Menu')
st.sidebar.header('Select Parameters')

idx = str(st.sidebar.number_input('Insert an index number between 0-1000 to select a random Story', min_value=0, max_value=10000, value=0))
st.write('Given index number : ', idx)
st.write('Online Id:', data[idx]['meta']['online_id'])
topx = st.sidebar.number_input('Insert most important x entity number to visualize', min_value=0, max_value=100, value=10)
st.write('Given top x entity index number : ', topx)

st.sidebar.header('Select Function for NER')
if st.sidebar.button('Show raw ner results dict   '):
    st.write('Raw results')
    st.write(data[idx])

def highlight_text(idx, topx):
    color_dict = {"CONSUMER_GOOD":"#800000",
    "OTHER":"#800080", "LOCATION":"#000080",'PERSON':"#808000",
    'WORK_OF_ART':"#808080",'ORGANIZATION':"#0000FF",'DATE': "#808080",
    'EVENT':"#808000",'PHONE_NUMBER':"#808080"}
    entity_list = data[idx]['ner_results']
    text = data[idx]['meta']['text']
    i=0
    for item in sorted(entity_list[0:topx], key=lambda x:x["begin_end_offset"][0]):
        if i == 0:
            white_begin = 0
            if item["begin_end_offset"][0] > 0:
                white_end = item["begin_end_offset"][0]-1
            else:
                white_end = 0
            white_text = text[white_begin:white_end]
            html_output = '<span class="nlp-display-others" style="background-color: white">{}</span>'.format(white_text)
            lab = item['entity'] + " - score " + str(round(item['salience']*100)) + " - idx " + item['entity_count']
            html_output += '<span class="nlp-display-entity-wrapper" style="background-color: {}"><span class="nlp-display-entity-name">{} </span><span class="nlp-display-entity-type">{}</span></span>'.format(
                        color_dict[item['entity']],
                        item['token'],
                        lab)
            white_begin = item["begin_end_offset"][1]
            i +=1
        else:
            white_end = item["begin_end_offset"][0]-1
            white_text = text[white_begin:white_end]
            html_output += '<span class="nlp-display-others" style="background-color: white">{}</span>'.format(white_text)
            lab = item['entity'] + " - score " + str(round(item['salience']*100)) + " - idx " + item['entity_count']
            html_output += '<span class="nlp-display-entity-wrapper" style="background-color: {}"><span class="nlp-display-entity-name">{} </span><span class="nlp-display-entity-type">{}</span></span>'.format(
                        color_dict[item['entity']],
                        item['token'],
                        lab)
            white_begin = item["begin_end_offset"][1]

    white_text = text[white_begin:len(text)]
    html_output += '<span class="nlp-display-others" style="background-color: white">{}</span>'.format(white_text)

    html_output += """</div>"""

    html_output = html_output.replace("\n", "<br>")

    html_content_save = style_config.STYLE_CONFIG_ENTITIES+ " "+html_output

    #st.markdown(display(HTML(html_content_save)))  
    components.html(html_content_save, width=800, height=1000)

def show_google_trends(token):

    pytrends = TrendReq(hl='de-GER', tz=360)

    pytrends.build_payload(kw_list=[token])

    time_df = pytrends.interest_over_time()

    # creating graph
    plt.style.use('bmh')
    register_matplotlib_converters()
    fig,ax = plt.subplots(figsize=(12, 6))
    time_df[token].plot(color='purple')
    # adding title and labels
    plt.title(f'Total Google Searches for {token}', fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Total Count')

    return st.pyplot(fig)

def google_trending_searches():
    pytrends = TrendReq(hl='de-GER', tz=360)
    return pytrends.trending_searches(pn='germany')


def text_2_speech(text):
    tts = gTTS(text, lang="de", slow=False)
    tts.save("1.wav")
    sound_file = open('1.wav','rb')
    audio_bytes = sound_file.read()
    return st.audio(audio_bytes, format='audio/ogg')

def googlepolly_tts(text, voice):
    polly = client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice)
    stream = response.get('AudioStream')
    with open('output_aws_polly.mp3', 'wb') as f:
        data = stream.read()
        f.write(data)

    sound_file = open('output_aws_polly.mp3','rb')
    audio_bytes = sound_file.read()
    return st.audio(audio_bytes, format='audio/ogg')

if st.sidebar.button('Show highlighted text     '):
    st.write('Online Id:', data[idx]['meta']['online_id'])
    st.write('Highlighted text')
    highlight_text(idx, topx) 

st.sidebar.header('Select Parameter and Function for G-Trends')

entity_idx = st.sidebar.number_input('Select entity index number for Google Trends', min_value=0, max_value=20, value=0)
token = data[idx]['ner_results'][entity_idx]['token']
st.sidebar.write(f'You have selected entity index  "{entity_idx}" token : {token}')

if st.sidebar.button(f'Show Google Trends Graph for "{token}" '):
    show_google_trends(token)

if st.sidebar.button(f'Show Google Trending Searches in Germany'):
    st.write(google_trending_searches())

st.sidebar.header('Select Parameter and Function for Voice')

voice = st.sidebar.selectbox('Select voice', ['Amelie'])
if st.sidebar.button(f'Run open source Text-2-Speech'):
    text = data[idx]['meta']['text']
    text_2_speech(text)

voice = st.sidebar.selectbox('Select voice', ['Vicki', 'Marlene','Hans'])

if st.sidebar.button(f'Run AWS Polly Text-2-Speech'): 
    text = data[idx]['meta']['text']
    googlepolly_tts(text, voice)

