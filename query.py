import os
import re 
from tokenizer import tokenize
from collections import defaultdict
from nltk.stem import SnowballStemmer
from operator import itemgetter
from math import log
import json

if __name__ == "__main__":
    docs = 55393
    index_file = "./indices/dev_index.json"  # Path to save the index file
    url_mapping_file = "url_mapping.json"  # Path to save the URL mappings
    stemmer = SnowballStemmer("english")
    tf_idf_scores = defaultdict(float)
    query = input('Please enter your query: \n')
    tokens = tokenize(query, stemmer)
   
    with open(index_file, 'r', encoding = 'utf-8') as i:
        data = json.load(i)
        for word in tokens:
            postings = data[word]
            idf = log(docs/len(postings))
            for p in postings:
                tf_idf_scores[p[0]] += float(p[1]*idf) #Need to change?

    res = dict(sorted(tf_idf_scores.items(), key=itemgetter(1), reverse=True)[:10]).keys()
    print (f"Top 10 results for {query}: \n ")
    with open (url_mapping_file, 'r', encoding = 'utf-8') as f:
        data2 = json.load(f)
        i = 1
        for keys in res:
            print (f"{i}: {(data2[str(keys)])[0]}\n")
            i+=1


