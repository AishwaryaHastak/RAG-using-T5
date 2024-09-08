from src.pipeline import RAGPipeline

if __name__ == "__main__":
    pipeline = RAGPipeline()
    # query = "What is the difference between extend and append?"
    query = "How to retrain this same model whenever new data comes in, without losing the predictive power of the model?"
    # query = "I an running a CUDA program and I am getting this error: cudaGetDeviceCount returned 38, no CUDA-capable device is detected."
    response = pipeline.get_response(query,3)
    print(response)
