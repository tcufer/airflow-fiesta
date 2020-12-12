#!/usr/bin/env python

import csv
import yaml
from datetime import datetime
from bs4 import BeautifulSoup 
import requests
import hashlib 
import re

class GoodreadsReader():

    BASE_URL = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q="
    
    def compose_url(self, tags):
        tags_to_string = ""
        if len(tags) > 1:
            tags_to_string = tags[0]
            tags.pop(0)
            for tag in tags:
                tags_to_string = tags_to_string + "+" + tag
        elif len(tags) == 1:
            tags_to_string = tags[0]
        
        composed = "%s%s&commit=Search"%(self.BASE_URL, tags_to_string)
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
        # pages = soup.find_all("a", {"href": re.compile("page")})
        # for page in pages:
        for quote in soup.find_all("div", class_= "quote"):
            squote = {}
            squote['text']= quote.find("div", {"class": "quoteText"}).text.replace('\n','').strip()
            squote['author'] = quote.find("span", {"class": "authorOrTitle"}).text.replace('\n','').strip()  
            leftAlignedImage = quote.find("a", {"class": "leftAlignedImage"})
            squote['image'] = leftAlignedImage.img['src'] if leftAlignedImage else None
            quoteFooter = quote.find("div", {"class": "quoteFooter"})
            squote['tags'] = [tag.text.strip() for tag in quoteFooter.find_all("a") if tag and "likes" not in tag.text]
            squote['likes'] = quoteFooter.find("div", {"class": "right"}).text.strip()
            squote['id'] = self.generate_quote_id(squote['text'] + squote['author'])
            results.append(squote)
        
        #write to csv
        file_name = './store_files/goodreads_quotes_{}.csv'.format(timestamp)
        with open(file_name, 'w+') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(results[0].keys())
            for row in results:
                writer.writerow(row.values())
            print('{} was successfully created.'.format(file_name))
        pass

if __name__ == '__main__':
    GoodreadsReader().get_quotes()