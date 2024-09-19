# app.py
 
import streamlit as st
import time
import uuid

from src.vectorpipeline import VecSearchRAGPipeline
from src.espipeline import ElSearchRAGPipeline
from src.setup_db import (
    init_db,
    save_conversation,
    save_feedback,
    get_recent_conversations,
    get_feedback_stats,
)


def print_log(message):
    print(message, flush=True)

def main():
    print_log("Starting the Data Science Assistant application")
    st.title("Data Science Assistant")

    # Initialize the database
    init_db()
    
    # Check if the index has been created already
    text_index_created = st.session_state.get("text_index_created", False)
    vec_index_created = st.session_state.get("vec_index_created", False)

    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )
    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    # Search type selection
    search_type = st.radio("Select search type:", ["Text", "Vector"])
    print_log(f"User selected search type: {search_type}")

    if search_type == "Text":
        pipeline = ElSearchRAGPipeline()
        # Automatically create index if not already created
        if not text_index_created:
            with st.spinner("Generating vector embeddings..."):
                print_log("Generating vector embeddings...")
                pipeline.read_data()
            with st.spinner("Creating index..."):
                print_log("Indexing data...")
                pipeline.create_index(pipeline.data_dict)
                st.success("Index created!")
                st.session_state.text_index_created = True  
    else:
        pipeline = VecSearchRAGPipeline()
        # Automatically create vector index if not already created
        if not vec_index_created:
            with st.spinner("Reading data..."):
                print_log("Reading data...")
                pipeline.read_data()
            with st.spinner("Creating index..."):
                print_log("Indexing data...")
                pipeline.create_index(pipeline.data_dict)
                st.success("Index created!")
                st.session_state.vec_index_created = True   

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Ask"):
        print_log(f"User asked: '{user_input}'")
        with st.spinner("Processing..."):
            print_log(
                f"Getting answer from assistant using {search_type} search"
            )
            start_time = time.time()
            answer_data = pipeline.get_response(user_input)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(answer_data)

            # Save conversation to database
            print_log("Saving conversation to database")
            save_conversation(
                st.session_state.conversation_id, user_input, answer_data,
            )
            print_log("Conversation saved successfully")
            st.session_state.conversation_id = str(uuid.uuid4())

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('👍', key='positive'):
            st.session_state.count += 1
            print_log(
                f"Positive feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, 1)
            print_log("Positive feedback saved to database")
            st.write('Thank you for the positive feedback!')
    with col2:
        if st.button('👎', key='negative'):
            st.session_state.count -= 1
            print_log(
                f"Negative feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, -1)
            print_log("Negative feedback saved to database")
            st.write('Sorry to hear that. We appreciate your feedback!')

    # Display recent conversations
    st.subheader("Recent Conversations")
    recent_conversations = get_recent_conversations(limit=3)
    for conv in recent_conversations:
        st.write(f"Q: {conv['question']}")
        st.write(f"A: {conv['answer']}")
        st.write("---")

    # Display feedback stats
    feedback_stats = get_feedback_stats()
    st.subheader("Feedback Statistics")
    st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
    st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")


print_log("Streamlit app loop completed")


if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()