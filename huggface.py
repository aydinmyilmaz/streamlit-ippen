from transformers import pipeline
import streamlit as st

def app():
    qa_pipeline = pipeline(
                "question-answering",
                model="deepset/gelectra-base-germanquad"
    )

    add_selectbox = st.sidebar.selectbox(
    "Select NLP Function?",
    ("Summarization", "QA")
)
    if add_selectbox == "QA":

        option = st.selectbox(
                    'Select an option',
                    ('', 'Use Uploaded Text', 'Insert Own Text'))

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
            st.write('Context\n\n', context)
            question = "Wie Sonnenmassen entstehen?"
            st.write('Question\n\n', question)

        if option == 'Insert Own Text':
        
            context = st.text_area("Enter context", "", key="1")
            st.write('Context\n\n', context)
            question = st.text_area("Enter question", "", key="2")
            st.write('Question\n\n', question)
        
        if st.button('Show Answer'):
            response = qa_pipeline({
                "context": context,
                'question': question
            })
            st.write('Answer\n\n', response['answer'])

    else:
        st.write("coming soon...")
