import chromadb
import glob
import json
from tqdm import tqdm
from InstructorEmbedding import INSTRUCTOR
import os
import constants as cts
import subprocess

class GetNearestLinks:
    def __init__(self, query) -> None:
        # query string
        self.query = query
        # check if chromadb data folder ready
        if not os.path.isdir(cts.CHROMADB_PERSISTANT_DATA_FOLDER):
            # unzip data folder
            subprocess.run(["unzip", cts.CHROMADB_DATA_ZIP_FILE_PATH, "-d", cts.CHROMADB_PERSISTANT_DATA_FOLDER])
        # chromadb persistent data folder
        self.chromadb_folder = cts.CHROMADB_PERSISTANT_DATA_FOLDER
        # initialize chromadb client
        self.chroma_client = chromadb.PersistentClient(path=self.chromadb_folder)
        # chromadb collection name
        self.collection_name = cts.CHROMADB_COLLECTION_NAME
        # get or create collection in chromadb
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        # instructor model to use for embeddings
        self.instructor_model = cts.CHROMADB_EMBEDDING_MODEL
        # pick InstructGPT model
        self.model = INSTRUCTOR(self.instructor_model)
            
    def get_links(self) -> dict:                
        # prompt for creating embeddings for the search string
        prompt = "Represent the question for retrieving supporting documents"
        # create embeddings for the search string
        query_embeddings = self.model.encode(
            sentences=[[prompt, self.query]], 
            show_progress_bar=False
            ).squeeze().tolist()
        # get closest documents for the search string embeddings
        results = self.collection.query(
            query_embeddings=query_embeddings, 
            n_results=3)
        return results['ids'][0]