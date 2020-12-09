#!/usr/bin/env python

# import csv
# import pdb
# import yaml
# import re
# from datetime import datetime
from bs4 import BeautifulSoup 
import requests
import pprint
# class GoodreadsReader():

#     def get_qutoes(self):
#         #@TODO


if __name__ == '__main__':
    # GoodreadsReader().get_quotes()
    results = []
    url = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=stoicism&commit=Search"   
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