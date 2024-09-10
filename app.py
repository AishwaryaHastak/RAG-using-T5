import streamlit as st
from src.vectorpipeline import VecSearchRAGPipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import Feedback, DATABASE_URL

# Database setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the VecSearchRAGPipeline
pipeline = VecSearchRAGPipeline()
data_dict = []
index_created = False

def index_data():
    global index_created
    st.session_state.index_status = "Reading data..."
    data_dict = pipeline.read_data()

    st.session_state.index_status = "Indexing started. Please wait for a while..."
    pipeline.create_index(data_dict)
    index_created = True
    st.session_state.index_status = "Indexing completed!"

def save_feedback(question, response, feedback):
    db = SessionLocal()
    try:
        new_feedback = Feedback(question=question, response=response, feedback=feedback)
        db.add(new_feedback)
        db.commit()
    except Exception as e:
        st.error(f"Error saving feedback: {e}")
        db.rollback()
    finally:
        db.close()

# Streamlit app interface
st.title('Vector Search and LLM Response')

if 'index_status' not in st.session_state:
    st.session_state.index_status = ""

if st.session_state.index_status:
    st.write(st.session_state.index_status)

if st.button('Start Indexing'):
    if not index_created:
        with st.spinner('Generating embeddings, please wait...'):
            index_data()
    else:
        st.write("Index already created!")

# Form for query submission
with st.form(key='query_form'):
    query = st.text_input("Enter your query")
    submit_button = st.form_submit_button(label='Submit Query')

if submit_button:
    if not query:
        st.error('Please enter a query')
    else:
        st.write('Generating response...')
        results = pipeline.search(data_dict, query, 3)
        prompt = pipeline.generate_prompt(query, results)
        llm_response = pipeline.generate_response(prompt)
        st.write(f"Response: {llm_response}")

        # Feedback Buttons with State Management
        if 'feedback' not in st.session_state:
            st.session_state.feedback = None

        col1, col2 = st.columns(2)
        with col1:
            if st.button('👍', key='positive'):
                st.session_state.feedback = 'positive'
                st.write('Thank you for the positive feedback!')
        with col2:
            if st.button('👎', key='negative'):
                st.session_state.feedback = 'negative'
                st.write('Sorry to hear that. We appreciate your feedback!')

        if st.session_state.feedback:
            st.write('Saving feedback...')
            save_feedback(query, llm_response, st.session_state.feedback)
            st.session_state.feedback = None

