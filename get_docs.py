# import libraries
import constants as cts
import json

class GetDocuments:
    def __init__(self, query_urls: list) -> None:
        # json file path
        self.summaries_file_path = cts.SUMMARIES_FILE_PATH
        # all summaries
        self.summaries = None
        # urls to get docs for 
        self.query_urls = query_urls
        
    def get_documents(self) -> list:
        # read sumamries json file
        self.summaries = self.read_summaries_file()
        
        # get relevant docs from summaries collection 
        docs = []
        for url in self.query_urls:
            doc = self.summaries[url]
            if doc:
                docs.append(doc)   
        return docs
    
    def read_summaries_file(self) -> dict:
        # read file from json
        with open(self.summaries_file_path, 'r', encoding='utf-8') as f:
            json_dict = json.load(f)
        
        if json_dict:
            return json_dict['summaries']
        else:
            print('failed to retrive summaries from file')
            return {}