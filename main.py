import html
import os
import json
from postings import Posting
from analyitics import Analyitics

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import re

from lxml import etree

def index_builder():
    index = {}
    main_folder = "/DEV"
    #main_folder = "/TestPages"
    doc_id = 0

    for root, files in os.walk(main_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
        
        with open(filename, 'r') as web_page:
            try:
                json_data = json.load(web_page)
        
                #Maybe build helper function that can load html content tag by tag/line by line?
                web_content = json_data.get("content")
                docposting = tokenize(web_content)
                #for key in docposting:
                    #if docposting key in index:
                        #index[key].append([url, docposting[key][0], docposting[key][1], docposting[key][2]])
                    #else
                        #index[key] = [url, docposting[key][0], docposting[key][1], docposting[key][2]]
                
                
                web_url = json_data.get("url")

                doc_id += 1
                #Add mapping of doc_id to actual URL on url_mapping.txt
                with open("url_mapping.txt", "w") as mapping:
                    mapping.write(f"{doc_id} -> {web_url}\n")

                #tokens = tokenize(web_content)
                #insert tokenized content into index:
                # for token in tokens:
                #     index[token] = Posting(doc_id, f_count...)
                
            except Exception as e:
                print("The following error has occured: ", e)

    #Don't return in memory dictionary but write it into seperate file
    return index

def tokenize(web_content) -> dict:
    '''Accepts string of web_content, returns dict where key=token and value=[[tokens]]'''
    tree = html.fromstring(web_content)
    tokens_by_tag = {}
    pattern = re.compile(r'\b\w+\b') #Regex pattern to filter out punctuation
    position_counter = 0 #keep track of position of each token
    for element in tree.iter():
        tag_name = element.tag.lower()
        text = element.text
        if text: #tokenize and remove punctuation
            tokens = word_tokenize(text)
            filtered_tokens = [token for token in tokens if pattern.match(token)]
            for token in filtered_tokens:
                stemmed_token = stemmer.stem(token.lower())
                if stemmed_token in tokens_by_tag:
                    tokens_by_tag[stemmed_token][0].append(tag_name)
                    tokens_by_tag[stemmed_token][1].append(position_counter)
                    tokens_by_tag[stemmed_token][2] += 1
                else:
                    tokens_by_tag[stemmed_token] = ([tag_name], [position_counter], 1)
                position_counter += 1
        return tokens_by_tag
    
    #EXAMPLE OF EXPECTED OUTPUT:
    # for token, (tags, positions, frequency) in tokens_by_tag.items():
    # print(f"Token '{token}': ({tags}, {positions}, {frequency})")
    

def main():
    index = index_builder()
    with open("index.json", "w") as outfile:
        json.dump(index, outfile)
    #json_file.write(f"{{key} : {Posting}}")
    data = Analyitics("index.json")
    #data = Analyitics(index)
    document_count = data.get_document_count()
    token_count = data.get_token_count()
    index_size = data.get_index_size()
    with open("data_report.txt", "w") as report:
        report.write(f"Total Number of Indexed Documents: {document_count}\n\n")
        report.write(f"Total Number of Unique Tokens: {token_count}\n\n")
        report.write(f"Total Size of Index: {index_size}\n\n")

    

                    
if __name__ == "__main__":
    nltk.download('punkt')
    stemmer = PorterStemmer
    print("Testing main now")
    main()
