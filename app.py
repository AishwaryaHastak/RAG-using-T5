# app.property
 
import streamlit as st
import time
import uuid

from src.vectorpipeline import VecSearchRAGPipeline
from src.espipeline import ElSearchRAGPipeline
from setup_db import (
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
    st.title("Course Assistant")

    # Initialize the database
    init_db()
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
    else:
        pipeline = VecSearchRAGPipeline()

    if st.button("Create Index"):
        with st.spinner("Reading data/Generating vector embeddings..."):
            print_log("Reading data...")
            pipeline.read_data()
        with st.spinner("Creating index..."):
            print_log("Indexing data...")
            pipeline.create_index(pipeline.data_dict)
            st.success("Index created!")

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

            # Display monitoring information

            # Save conversation to database
            print_log("Saving conversation to database")
            save_conversation(
                st.session_state.conversation_id, user_input, answer_data,
            )
            print_log("Conversation saved successfully")
            # Generate a new conversation ID for next question
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

    # st.write(f"Current count: {st.session_state.count}")

    # Display recent conversations
    st.subheader("Recent Conversations")
    # relevance_filter = st.selectbox(
    #     "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]
    # )
    recent_conversations = get_recent_conversations(
        limit=3
    )
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