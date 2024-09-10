# main.py 

from src.mspipeline import MiniSearchRAGPipeline
from src.espipeline import ElSearchRAGPipeline
from src.vectorpipeline import VecSearchRAGPipeline

if __name__ == "__main__":
    # # Perform the search and generate the response using MiniSearch Engine
    # pipeline = MiniSearchRAGPipeline()
    # # Perform the search and generate the response using ElasticSearch
    # pipeline = ElSearchRAGPipeline()
    # Perform the search and generate the response using ElasticSearch and Vector Embeddings
    pipeline = VecSearchRAGPipeline()
    query = [   "How to manage model versioning in Machine Learning?",
                "What’s the trade-off between bias and variance?",
                "What are some common challenges in deploying a RAG model in production and how can they be addressed?"]
    response = pipeline.rag_pipeline(query[0],3, create_new_index = True)
    print(response)
