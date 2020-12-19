#!/usr/bin/env python

import csv
import yaml
from datetime import datetime
from bs4 import BeautifulSoup 
import requests
import hashlib 
import re

class GoodreadsReader():

    BASE_URL =  "https://www.goodreads.com"
    START_URL = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q="
    
    def compose_url(self, tags):
        tags_to_string = ""
        if len(tags) > 1:
            tags_to_string = tags[0]
            tags.pop(0)
            for tag in tags:
                tags_to_string = tags_to_string + "+" + tag
        elif len(tags) == 1:
            tags_to_string = tags[0]
        
        composed = "%s%s&commit=Search"%(self.START_URL, tags_to_string)
        return composed

    def generate_quote_id(self, data):
        prepared_value = hashlib.md5(data.encode())
        return prepared_value.hexdigest()

    def get_quotes(self):
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S')
        config = ""
        with open('./dags/secrets.yml', 'r') as file:
            config = yaml.safe_load(file)
        results = []
        url = self.compose_url(config['search_tags'])
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        pages = soup.find_all("a", {"href": re.compile("page")})
        page_urls = set()
        for page in pages:
            page_urls.add(self.BASE_URL + page['href'])
        page_urls.add(url)
        for page in page_urls:
            soup = BeautifulSoup(requests.get(page).text, "html.parser")
            print("Requesting page: ", page)
            for quote in soup.find_all("div", class_= "quote"):
                squote = {}
                squote['text']= quote.find("div", {"class": "quoteText"}).text.replace('\n','').strip()
                squote['author'] = quote.find("span", {"class": "authorOrTitle"}).text.replace('\n','').strip()
                quoteFooter = quote.find("div", {"class": "quoteFooter"})
                squote['tags'] = {tag.text.strip() for tag in quoteFooter.find_all("a") if tag and "likes" not in tag.text}
                squote['likes'] = int(quoteFooter.find("div", {"class": "right"}).text.replace(" likes", "").strip())
                squote['id'] = self.generate_quote_id(squote['text'] + squote['author'])
                results.append(squote)
        
        #write to csv
        file_name = './store_files/goodreads_quotes_{}.csv'.format(timestamp)
        with open(file_name, 'w+') as f:
            writer = csv.writer(f, delimiter='\t')
            for row in results:
                writer.writerow(row.values())
            print('{} was successfully created.'.format(file_name))
        pass
        return file_name

if __name__ == '__main__':
    GoodreadsReader().get_quotes()