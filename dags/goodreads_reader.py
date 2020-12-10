#!/usr/bin/env python

# import csv
# import pdb
import yaml
# import re
# from datetime import datetime
from bs4 import BeautifulSoup 
import requests
import pprint
# class GoodreadsReader():

#     def get_qutoes(self):
#         #@TODO

BASE_URL = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q="


def compose_url(tags):
    tags_to_string = ""
    if len(tags) > 1:
        tags_to_string = tags[0]
        tags.pop(0)
        for tag in tags:
            tags_to_string = tags_to_string + "+" + tag
    elif len(tags) == 1:
        tags_to_string = tags[0]
    
    composed = "%s%s&commit=Search"%(BASE_URL, tags_to_string)
    print(composed)
    return composed


if __name__ == '__main__':
    # GoodreadsReader().get_quotes()
    config = ""
    with open('./dags/secrets.yml', 'r') as file:
      config = yaml.safe_load(file)
    results = []
    url = compose_url(config['search_tags'])
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for quote in soup.find_all("div", class_= "quote"):
        squote = {}
        squote['text']= quote.find("div", {"class": "quoteText"}).text.replace('\n','').strip()
        squote['author'] = quote.find("span", {"class": "authorOrTitle"}).text.replace('\n','').strip()  
        leftAlignedImage = quote.find("a", {"class": "leftAlignedImage"})
        squote['image'] = leftAlignedImage.img['src'] if leftAlignedImage else None
        quoteFooter = quote.find("div", {"class": "quoteFooter"})
        squote['tags'] = [tag.text.strip() for tag in quoteFooter.find_all("a") if tag and "likes" not in tag.text]
        results.append(squote)
    
    pprint.pprint(results)
    
# https://github.com/CW4RR10R/Quotes-API