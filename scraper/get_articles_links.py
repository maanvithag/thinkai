# import libraries
import json
from bs4 import BeautifulSoup
import time
import requests
import constants as cts

class GetArticlesLinks:
    def __init__(self):
        # page url for all links to articles
        self.all_articles_page_url = cts.ALL_ARTICLES_PAGE_URL
        # folder path for json files
        self.scraped_links_file_path = cts.SCRAPED_LINKS_FILE_PATH
    
    def get_articles_links(self):
        # get all articles urls
        all_articles_links = self.get_links()  
    
        print('got all articles links, count is: ', len(all_articles_links))
            
        # form json dict to dump to file
        articles = {
            'count': len(all_articles_links),
            'articles': all_articles_links
        }
    
        # write json to file
        self.dump_to_file(articles)
    
    def get_links(self):
        # initialize list to store all links
        all_articles_links = []
    
        response = requests.get(self.all_articles_page_url)
        if response.status_code != 200:
            print('Page Not Found: Scraping Failed, Try Again')
        
        # get all response text
        soup = BeautifulSoup(response.text, 'html.parser')
        # get all article content
        all_content = soup.find('div', {"id":'content'})
        # get all articles link elements
        all_links_elements = all_content.find('ul').find_all('li')
        
        # extract url from each link element
        for link_ele in all_links_elements:
            article_url = link_ele.find('a').attrs['href']
            all_articles_links.append(article_url)
                                    
        return all_articles_links

    def dump_to_file(self, json_dict: dict) -> None:        
        with open(self.scraped_links_file_path, 'w') as f:
            json.dump(json_dict, f)  

    
if __name__ == "__main__":
    gal = GetArticlesLinks()
    gal.get_articles_links()