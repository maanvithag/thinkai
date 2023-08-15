# import libraries
import json
from collections import defaultdict
import random
import time
from bs4 import BeautifulSoup
import requests
import os
import constants as cts

class ArticleScraper:
    def __init__(self):
        # articles json file path
        self.articles_links_file_path = cts.SCRAPED_LINKS_FILE_PATH
        # folder path for articles scraped json files
        self.scraped_articled_folder_path = cts.SCRAPED_ARTICLES_FOLDER_PATH
        
    def scrape_all_articles(self):
        # dict to keep track of how many times a page timed out
        page_retries = defaultdict(int)
        
        # read articles json file
        with open(self.articles_links_file_path, 'r') as f:
            articles_dict = json.load(f)
        # get list of articles links
        articles = articles_dict['articles']
        
        # check if scraped articles folder exists,
        # if not, create one
        if not os.path.exists(self.scraped_articled_folder_path):
            print('creating scraped articles folder, path is: ', self.scraped_articled_folder_path)
            os.mkdir(self.scraped_articled_folder_path)
        
        # define offset for the articles links list in the json file
        offset_start = 0
        offset_end = len(articles)
        
        print('total number of pages to scrape: ', offset_end - offset_start)
        
        pages_offset = offset_start
        while pages_offset < offset_end:
            print('scraping pages from ', pages_offset)
            
            # get the offset where scraping stopped
            pages_offset = self.article_scraper(articles, pages_offset, offset_end)
            
            # keep track if a scraping a page is failing after multiple retries
            # if yes, skip it!
            page_retries[pages_offset] = (page_retries.get(pages_offset, 0)) + 1
            if page_retries[pages_offset] > 2:
                print('skipping page, ', articles[pages_offset])
                pages_offset += 1
            
            # when scraping stops, usually due to timeout issues, wait for a few seconds before scraping
            sleep_seconds = random.randint(10, 20)
            print(f'sleeping for {sleep_seconds} seconds')
            time.sleep(sleep_seconds)
    
    def article_scraper(self, page_urls: list, pages_offset: int, offset_end: int):
    
        while pages_offset < offset_end:
                
            page_url = page_urls[pages_offset]        
            print('current page offset is: ', pages_offset, page_url)

            # ping url
            response = requests.get(page_url)
        
            # check if valid page
            if response.status_code != 200 or 'entries' not in page_url:
                print('page not found, skipping, current page offset is: ', pages_offset, page_url)
                pages_offset += 1
                continue
            
            # parse html response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # get all article content
            article_content = soup.find('div', {"id":"aueditable"})
            
            if article_content:
                # initialize article json
                article_json = {
                    'url': page_url,
                    'title': '',
                    'published_date': '',
                    'summary': '',
                    'content': ''
                }
                
                # get article title
                article_title_tag = article_content.find('h1')
                if article_title_tag: 
                    article_json['title'] = article_title_tag.text
                
                # get article published date
                article_pubinfo_tag = article_content.find('div', {"id":"pubinfo"})
                if article_pubinfo_tag: 
                    article_json['published_date'] = article_pubinfo_tag.find('em').text
                    
                # get article summary
                article_summary_tag = article_content.find('div', {"id":"preamble"})
                if article_summary_tag:
                    article_json['summary'] = article_summary_tag.text.replace('\n', ' ')
                    
                # get article main text
                article_main_text_tag = article_content.find('div', {"id":"main-text"})
                if article_main_text_tag:
                    article_json['content'] = article_main_text_tag.text.replace('\n', ' ')
                    
                # form file name from url
                url_split = page_url.split('/')
                page_file_name = '_'.join(url_split[3:-1])
                
                # form page file path
                page_file_path = self.scraped_articled_folder_path + page_file_name + '.json'
                
                # dump to json file
                with open(page_file_path, 'w', encoding='utf-8') as f:
                    json.dump(article_json, f)
                
            # increment pages offset
            pages_offset = pages_offset + 1
                    
        return pages_offset
    
if __name__ == "__main__":
    asr = ArticleScraper()
    asr.scrape_all_articles()
    