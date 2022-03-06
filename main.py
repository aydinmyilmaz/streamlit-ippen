import streamlit as st
import json 
from IPython.display import display, HTML
import style_utils as style_config
import streamlit.components.v1 as components

st.title('Analyse NER')

path = "data_5000.json"

with open(path, 'r') as json_file:
    data = json.load(json_file)

idx = str(st.sidebar.number_input('Insert an index number', min_value=0, max_value=10000, value=0))
st.write('Given index number : ', idx)

topx = st.sidebar.number_input('Insert most important x entity number', min_value=0, max_value=100, value=10)
st.write('Given top x number : ', topx)

if st.button('Show raw results'):
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
            lab = item['entity'] + " - score "+str(round(item['salience']*100))+" - idx "+item['entity_count']
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
            lab = item['entity'] + " - score "+str(round(item['salience']*100))+" - idx "+item['entity_count']
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
    components.html(html_content_save, width=800, height=3000)


if st.button('Show highlighted text'):
    st.write('Online Id:', data[idx]['meta']['online_id'])
    highlight_text(idx, topx)   