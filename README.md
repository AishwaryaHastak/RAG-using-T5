# End-to-End RAG System for Data Science Q&A

This project presents an end-to-end Retrieval-Augmented Generation (RAG) system specifically designed for handling questions and answers in the Data Science domain. The system integrates various advanced technologies for efficient retrieval and generation of responses.

## 🛠️ Tools Used

- **Python**: Programming language used for development.
- **Streamlit**: Framework for building the interactive web application.
- **Docker**: For containerizing the application and ensuring consistent deployment.
- **SQLAlchemy**: ORM for database interactions.
- **Flan-T5**: Language model from Hugging Face for response generation.
- **Sentence Transformers**: For generating vector embeddings of documents.
- **Elastic Search**: Scalable search engine for complex queries.
- **ChatGPT**: Used for generating synthetic data and creating a ground truth dataset.

## 📊 Dataset

The project utilizes a custom dataset, `data.csv`, which comprises a diverse collection of question and answer pairs. These pairs were generated using ChatGPT-3.5 and cover a wide range of topics and domains within Data Science. The dataset includes:

- **Supervised Learning**
- **Unsupervised Learning**
- **Recommender Systems**
- **Neural Networks**

Moreover, it addresses various aspects of the Machine Learning lifecycle such as:

- **Model Development**
- **Model Evaluation**
- **Model Deployment**

The dataset is designed to be comprehensive, ensuring coverage of both foundational and advanced topics, making it suitable for robust testing and evaluation of the RAG system.

## 🔍 Retrieval Component

The RAG system incorporates two methods for indexing and retrieving relevant documents:

1. **Simple Search Algorithm**:
   - Implemented in `minisearch.py`.
   - Utilizes **TF-IDF** for document indexing.
   - Employs **cosine similarity** to find and rank similar documents.

2. **Elastic Search**:
   - Offers a scalable and sophisticated search engine solution for handling more complex queries and retrieval needs.

## ✨ Generation Component

For generating responses, the system uses the open-source **Flan-T5** model from the Hugging Face library. Flan-T5 is a state-of-the-art language model designed to generate coherent and contextually accurate responses based on the retrieved information.

## 🔄 Vector Search

Vector search is performed by generating embeddings of documents using the **Sentence Transformers** library. This approach allows for precise and efficient retrieval by comparing vector representations of documents.

## 📈 Evaluation

The performance of the RAG system is assessed through:

1. **Ground Truth Dataset Creation**:
   - Developed using ChatGPT to establish a benchmark for evaluation.

2. **Evaluation Metrics**:
   - **Mean Reciprocal Rank (MRR)** and **Hit Rate** are calculated. 

### Achieved a Hit Rate of 0.87 and an MRR of 0.85

## 🌐 Deployment

The system is deployed as a **Streamlit** application, providing an interactive user interface. The deployment is managed using **Docker**, ensuring consistency and scalability of the application.

## 👍 Feedback Mechanism

A feedback mechanism is integrated to collect user feedback on the responses. Users can provide feedback using thumbs up 👍 or thumbs down 👎 buttons. Feedback is stored in an **SQL database**, which assists in ongoing model monitoring and improvement.

## Acknowledgements

Detailed steps on how to use ElasticSearch in python
https://dylancastillo.co/posts/elasticseach-python.html#create-a-local-elasticsearch-cluster
