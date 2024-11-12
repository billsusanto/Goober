import html
import os
import json
from postings import Posting

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import re

from lxml import etree

#Change later
#page_count = 0

def main():
    #index = {}
    main_folder = "/DEV"
    doc_id = 0

    for root, files in os.walk(main_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
        
        with open(filename, 'r') as web_page:
            try:
                json_data = json.load(web_page)
        
                web_content = json_data.get("content")
                web_url = json_data.get("url")

                doc_id += 1
                #Add mapping of doc_id to actual URL on url_mapping.txt
                with open("url_mapping.txt", "w") as mapping:
                    mapping.write(f"{doc_id} -> {web_url}")

                #tokens = tokenize(web_content)
                #insert tokenized content into index:
                # for token in tokens:
                #     index[token] = Posting(doc_id, f_count...)
                
            except Exception as e:
                print("The following error has occured: ", e)

def tokenize(web_content) -> dict:
    '''Accepts string of web_content, returns dict where key=token and value=list of tags where token was found'''
    tree = html.fromstring(web_content)
    tokens_by_tag = {}
    pattern = re.compile(r'\b\w+\b') #Regez pattern to filter out punctuation
    for element in tree.iter():
        tag_name = element.tag.lower()
        text = element.text
        if text: #tokenize and remove punctuation
            tokens = word_tokenize(text)
            filtered_tokens = [token for token in tokens if pattern.match(token)]
            for token in filtered_tokens:
                stemmed_token = stemmer.stem(token.lower())
                if stemmed_token in tokens_by_tag:
                    tokens_by_tag[stemmed_token].append(tag_name)
                else:
                    tokens_by_tag[stemmed_token] = [tag_name]
        return tokens_by_tag

                    
if __name__ == "__main__":
    nltk.download('punkt')
    stemmer = PorterStemmer
    print("test")
    main()