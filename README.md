# Data Science Q&A Application

This project is designed to provide precise answers to a broad range of Data Science and Machine Learning Lifecycle questions. Whether you're looking for explanations of concepts or advice on improving your ML models, this app is here to help! 🚀

## 📈Project Overview

This application utilizes a dataset of over 600 question-answer pairs covering various Data Science topics. It offers concise and relevant responses to your queries, including use-case specific questions such as "My regression model is overfitting on data, how can I improve its performance?" 

## RAG Flow

The Retrieval-Augmented Generation (RAG) flow combines a knowledge base with a language model to deliver accurate responses:

- **Knowledge Base:** Contains a Data Science Q&A dataset stored in `data.csv`.
- **Language Model:** Uses **Flan-T5**, an open-source model from Google available on Hugging Face, for augmented response generation.

## 📊 Retrieval Evaluation

The performance of retrieval methods was assessed using `ground-truth.csv`. The following methods were evaluated:

- **ElasticSearch:** 
  - **Hit Rate:** 0.87 
  - **Mean Reciprocal Rank (MRR):** 0.85
  - Best performing retrieval method with combined Question-Answer vector embedding.
  
- **Minisearch:** 
  - Competitive results but not as optimal as ElasticSearch.

- **Hybrid Search:** 
  - Did not achieve the best accuracy or performance compared to ElasticSearch.

Detailed results can be found in `evaluation.ipynb`. 

## 🔍 RAG Evaluation

The RAG pipeline was evaluated against the ground truth dataset using the cosine similarity metric. The system achieved a cosine similarity score of **0.8**, reflecting strong alignment with the expected results. 

![alt text](image.png)

## 🖥️ User Interface

The application features a simple and intuitive UI built with **Streamlit**. Users can easily input queries and view responses through a straightforward interface. 

## Ingestion Pipeline

A Python script handles the data ingestion process:

1. **Ground Truth Dataset Creation**:
   - Developed using ChatGPT to establish a benchmark for evaluation.

2. **Evaluation Metrics**:
   - **Mean Reciprocal Rank (MRR)** and **Hit Rate** are calculated.
   - Both metrics achieved an approximate score of 0.83, indicating high effectiveness in the retrieval and generation process.

## 🌐 Deployment

The system is deployed as a **Streamlit** application, providing an interactive user interface. The deployment is managed using **Docker**, ensuring consistency and scalability of the application.

## 👍 Feedback Mechanism

A feedback mechanism is integrated to collect user feedback on the responses. Users can provide feedback using thumbs up 👍 or thumbs down 👎 buttons. Feedback is stored in an **SQL database**, which assists in ongoing model monitoring and improvement.

## Acknowledgements

Detailed steps on how to use ElasticSearch in python
https://dylancastillo.co/posts/elasticseach-python.html#create-a-local-elasticsearch-cluster
