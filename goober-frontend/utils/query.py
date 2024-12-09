from tokenizer import tokenize
from nltk.stem import SnowballStemmer
from operator import itemgetter
import json
from math import log
import time


if __name__ == "__main__":
    docs = 55391
    stemmer = SnowballStemmer("english")
    q = {}
    tags = {}
    mapping = {}
    token_freq = []
    
    try:
        # First attempt: original paths
        index_path = "final_indicies"
        url_mapping_file = "url_mapping.json"

        with open(url_mapping_file, "r") as f:
            data = json.load(f)
            mapping = data

        with open(f"{index_path}/index_0.json", "r") as t:
            data = json.load(t)
            tags = data

    except FileNotFoundError as e:
        #print(f"Error: {e}. Trying alternative paths...")

        # Fallback: alternative paths
        index_path = "./final_indicies"
        url_mapping_file = "./url_mapping.json"

        try:
            with open(url_mapping_file, "r") as f:
                data = json.load(f)
                mapping = data

            with open(f"{index_path}/index_0.json", "r") as t:
                data = json.load(t)
                tags = data

        except FileNotFoundError as e:
            # If fallback paths also fail
            #print(f"Failed to load files from alternative paths: {e}")
            raise  # Re-raise the exception after logging
    

    query = input()
    start_time = time.perf_counter()
    tokens = tokenize(query, stemmer)
    for token in tokens:
        token_freq.append([token,len(data[token])])
    token_freq.sort(key = lambda x: x[1])
    for i in range(0,len(token_freq)):
        max_tag = 1
        if (i == 0):
            for j in range(55391):
                try:
                    posting = tags[token_freq[i][0]][j]
                    if j == 0: 
                        max_tag = posting[2]
                    q[posting[0]] = (log(posting[2]) + log(docs/token_freq[i][1])) *posting[2]/max_tag
                except:
                    continue
        else:
            max_tag = tags[token_freq[i][0]][0][2]
            for p in tags[token_freq[i][0]]:
                if p[0] in q:
                    q[p[0]] += (log(p[2]) + log(docs/token_freq[i][1]) )* p[2]/max_tag

    #print(q)
    res = dict(sorted(q.items(), key=itemgetter(1), reverse=True)[:10]).keys()
    for r in res:
        print(mapping[str(r)][0])
        #print(f'{mapping[str(r)][2]}\n\n')
    end_time = time.perf_counter()
    print(f"Time to tokenize query: {end_time - start_time:.6f} seconds")
