from transformers import pipeline
import streamlit as st
import torch
from transformers import BertTokenizerFast, EncoderDecoderModel


@st.cache(allow_output_mutation=True)
def load_qa_pipeline():

    qa_pipeline = pipeline(
                "question-answering",
                model="deepset/gelectra-base-germanquad"
            ) 
    return qa_pipeline

qa_pipeline = load_qa_pipeline()

# @st.cache(allow_output_mutation=True)
# def load_summarization_model():
#     ckpt = 'mrm8488/bert2bert_shared-german-finetuned-summarization'
#     tokenizer = BertTokenizerFast.from_pretrained(ckpt)
#     model = EncoderDecoderModel.from_pretrained(ckpt)

# model, tokenizer, device = load_summarization_model()

# def generate_summary(text):
#    inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
#    input_ids = inputs.input_ids.to(device)
#    attention_mask = inputs.attention_mask.to(device)
#    output = model.generate(input_ids, attention_mask=attention_mask)
#    return tokenizer.decode(output[0], skip_special_tokens=True)

# @st.cache(allow_output_mutation=True)
# def load_generator_pipeline():
#     gen_pipe = pipeline('text-generation', 
#                 model="dbmdz/german-gpt2",
#                 tokenizer="dbmdz/german-gpt2")     
#     return gen_pipe

#gen_pipe = load_generator_pipeline()

def app():

    add_selectbox = st.sidebar.selectbox(
                        "Select NLP Function",
                        ("QA",
                        "Summarization", 
                        "Completion"))

    def qa():
        st.header('Question Answering')
        option = st.selectbox(
                    'Select an option',
                    ( '', 
                     'Use Uploaded Text', 
                     'Insert Own Text'))

        if option == 'Use Uploaded Text':
            context = """ Es wird erwartet, dass sich schwarze Löcher mit Sternmasse bilden,
                wenn sehr massive Sterne am Ende ihres Lebenszyklus 
                zusammenbrechen. Nachdem sich ein Schwarzes Loch gebildet hat, 
                kann es weiter wachsen,indem es Masse aus seiner Umgebung 
                absorbiert. Durch Absorption anderer Sterne und Verschmelzung mit 
                anderen Schwarzen Löchern können sich  supermassereiche Schwarze 
                Löcher mit Millionen von Sonnenmassen (M☉) bilden.  Es besteht 
                Konsens darüber, dass in den Zentren der meisten Galaxien
                supermassereiche Schwarze Löcher existieren."""
            st.write('**Text:**\n\n', context)
            question = "Wie Sonnenmassen entstehen?"
            st.write('**Question:**\n\n', question)

        if option == 'Insert Own Text':

            context = st.text_area("Enter text", "", key="1")
            st.write('**Text:**\n\n', context)
            question = st.text_area("Enter question", "", key="2")
            st.write('**Question:**\n\n', question)
        
        if st.button('Show Answer'):
            response = qa_pipeline({
                "context": context,
                'question': question
            })
            st.write('**Answer**\n\n', response['answer'])

    def summarization():
        option = st.selectbox(
                    'Select an option',
                    ('', 
                    'Use Uploaded Text', 
                    'Insert Own Text'))

        if option == 'Use Uploaded Text':
            context = """ Johannes Calvin (* 10. Juli 1509 in Noyon, Picardie; † 27. Mai 1564 in Genf) war unter den Reformatoren des 16. Jahrhunderts der bedeutendste systematische Theologe. Sein Hauptwerk, die Institutio Christianae Religionis, wird als eine „protestantische Summa“ bezeichnet. Die Verfolgung der französischen Protestanten unter König Franz I. zwang den Juristen, Humanisten und theologischen Autodidakten Calvin wie viele Gleichgesinnte zu einem Leben im Untergrund, schließlich zur Flucht aus Frankreich. Die Stadtrepublik Genf hatte bei seiner Ankunft dort (1536) gerade erst die Reformation eingeführt. Nach zweijähriger Tätigkeit wurden Farel und Calvin vom Stadtrat ausgewiesen. Als ihn der Stadtrat von Genf zurückrief, war Calvins Stellung wesentlich stärker als bei seinem ersten Genfer Aufenthalt. Er hatte Erfahrungen mit der Gemeindeorganisation gewonnen, die ihm jetzt zugutekamen. Im Herbst 1541 kam Calvin nach Genf und arbeitete umgehend eine Kirchenordnung aus. Calvins Rückhalt in den folgenden Jahren war das Pastorenkollegium (Compagnie des pasteurs). Der starke Zuzug verfolgter Hugenotten veränderte die Bevölkerungsstruktur Genfs und die Mehrheitsverhältnisse im Stadtrat, was 1555 zur Entmachtung der Calvin-kritischen Ratsfraktion führte."""
            st.write('**Text**\n\n', context)


        if option == 'Insert Own Text':
            context = st.text_area("Enter text", "", key="1")
            st.write('**Text**\n\n', context)
        
        if st.button('Show Summary'):
            #summarized = summarizer(context, min_length=75, max_length=300)
            summarized = generate_summary(context)
            st.write('**Answer**\n\n', summarized)

    # def completion():
    #     option = st.selectbox(
    #                 'Select an option',
    #                 ('', 
    #                 'Insert Text for Completion'))

    #     if option == 'Insert Text for Completion':
    #         sentence = st.text_area("Enter sentence", "", key="1")
    #         #text = gen_pipe(sentence, max_length=100)[0]["generated_text"]
            
        
    #     if st.button('Generate Text'):
    #         st.write('**Generated Text**\n\n', text)

    if add_selectbox == "QA":
        qa()
    
    # if add_selectbox == "Completion":
    #     completion()
    
    # if add_selectbox == "Summarization":
    #     summarization()
         

    else:
        st.write("coming soon...")
