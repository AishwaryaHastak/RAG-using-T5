# espipeline.py

import os
import pandas as pd 
from elasticsearch import Elasticsearch 
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.constants import model_name,index_name

class ElSearchRAGPipeline:
    def __init__(self): 
        self.query = None
        self.response = None
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.es = Elasticsearch("http://elasticsearch:9200")
        # self.es = Elasticsearch("http://localhost:9200")
        self.data_dict = None

    def read_data(self):
        """
        Reads data from csv file and converts it into list of dictionaries
        """
        print('[DEBUG] Reading data...')
        # Read data into dataframe 
        data_file_path = os.path.join('data', 'data.csv')
        df = pd.read_csv(data_file_path).dropna()

        # Convert dataframe to list of dictionaries
        self.data_dict = df.to_dict(orient="records")
        
    def create_index(self):
        print('\n\n[[DEBUG] Creating Index...')

        mappings = {
                "properties": {
                    "question": {"type": "text"},
                    "answer": {"type": "text"},
            }
        }
        
        # Create Index and delete if it already exists
        self.es.indices.delete(index=index_name, ignore_unavailable=True)
        self.es.indices.create(index=index_name, mappings=mappings)

        # Add Data to Index using index()
        print('\n\n[[DEBUG] Adding data to index...')
        # Considering only the first 100 rows for now
        for i in tqdm(range(len(self.data_dict))):
            row = self.data_dict[i]
            self.es.index(index=index_name, id=i, document=row)

        # helpers.bulk(es, data_dict)

    def search(self, query, num_results=3):
        """
        Retrieves results from the index based on the query.

        Args:
            data_dict (list of dict): List of dictionaries containing the data to be indexed.
            query (str): The search query string.
            num_results (int): The number of top results to return.

        Returns:
            list of str: List of results matching the search criteria, ranked by relevance.
        """
        # Retrieve Search Results
        print('\n\n[[DEBUG] Retrieving Search Results...') 
        results = self.es.search(
            index=index_name,
            size = num_results,
            query={
                    "bool": {
                        "must": {
                            "multi_match": {
                                "query": query,
                                "fields": ["question^3", "answer", "topic"],
                                "type": "best_fields",
                            }
                        },
                    },
                },
        )

        time_taken = results['took']
        relevance_score = results['hits']['max_score']
        total_hits = results['hits']['total']['value']
        topic = results['hits']['hits'][0]['_source']['topic']

        print('\n\n[DEBUG] Retrieved results:', time_taken, relevance_score, total_hits)
        result_docs = [hit['_source'] for hit in results['hits']['hits']] 

        response = [result['answer'] for result in result_docs]

        # print('\n\n[DEBUG] Retrieved results:', response)
        return response, time_taken, total_hits, relevance_score, topic
    
    def generate_prompt(self, query, response):
        """
        Generates a prompt for the LLM based on the query and response.

        Args:
            query (str): The search query string.
            response (str): The response from the retrieval model.

        Returns:
            str: The prompt to be sent to the LLM.
        """

        prompt_template = """
            You're a data science expert. 
            Provide concise and complete answers to the questions based on the context given below.
            QUESTION: {question}

            CONTEXT: 
            {response}
            """.strip()

        prompt = prompt_template.format(question=query, response=response)
        return prompt
    
    def generate_response(self, prompt): 
        """
        Generates a response using the LLM based on the given prompt.

        Args:
            prompt (str): The prompt to generate a response for.

        Returns:
            str: The generated response from the LLM.
        """

        print('[DEBUG] Generating LLM response...')
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            max_length=512, 
            truncation=True, 
            padding='max_length'
        )

        # Generate Response
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=1024,
            min_length=100,
            no_repeat_ngram_size=3,
            do_sample=True, 
            num_beams=4,        
            early_stopping = True # Stop once all beams are finished 
            # early_stopping = False # Stop once max_new_tokens is reached
        )
        
        llm_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return llm_response
    
    def get_response(self,query, num_results=3, create_new_index=False):
        """
        Retrieves and generates a response for a given query.

        Args:
            query (str): The search query string.
            num_results (int, optional): The number of top results to return. Defaults to 5.

        Returns:
            str: The generated response from the LLM.
        """
        if create_new_index:
            self.create_index()
        results, time_taken, total_hits, relevance_score, topic = self.search(query, num_results)
        prompt = self.generate_prompt(query, results)
        llm_response = self.generate_response(prompt)
        return llm_response, time_taken, total_hits, relevance_score, topic