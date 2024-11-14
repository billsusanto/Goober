from bs4 import BeautifulSoup
import os
import json
import nltk
from analyitics import Analyitics
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

def index_builder():
    index = {}
    main_folder = ".\DEV"
    doc_id = 0
    url_mappings = []  # Batch storage for URL mappings
    batch_size = 1000  # Define a batch size for periodic writing

    for root, dirs, files in os.walk(main_folder):
        print("Currently in directory:", root)
        print("It has this many files: ", len(files))
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", errors="ignore") as web_page:
                try:
                    json_data = json.load(web_page)
                    web_url = json_data.get("url")
                    web_content = json_data.get("content")

                    if not web_content.strip():  # Skip empty content
                        continue  

                    doc_id += 1
                    url_mappings.append(f"{doc_id} -> {web_url}\n")  # Store mapping in batch

                    # Tokenize content and add to index
                    docposting = tokenize(web_content)
                    for key in docposting:
                        if key in index:
                            index[key].append([doc_id, docposting[key][0], docposting[key][1], docposting[key][2]])
                        else:
                            index[key] = [doc_id, docposting[key][0], docposting[key][1], docposting[key][2]]
                    
                    # Write partial indexes every 1000 documents
                    if doc_id % 1000 == 0:
                        write_partial_index(index, doc_id)
                        index.clear()  # Clear memory after writing partial index

                    # Write url_mappings every batch_size entries
                    if len(url_mappings) >= batch_size:
                        with open("url_mapping.txt", "a") as mapping_file:
                            mapping_file.writelines(url_mappings)
                        url_mappings.clear()  # Clear memory after writing batch

                except Exception as e:
                    print("Error processing file:", e)

    # Write any remaining index and URL mappings
    write_partial_index(index, doc_id)  # Write any remaining index data
    with open("url_mapping.txt", "a") as mapping_file:
        mapping_file.writelines(url_mappings)  # Write remaining URL mappings


def tokenize(web_content) -> dict:
    stemmer = PorterStemmer()
    if not web_content:
        print("Empty document content detected, skipping.")
        return {}

    web_content = re.sub(r'[\x00-\x1F\x7F]', '', web_content)
    try:
        soup = BeautifulSoup(web_content, 'html.parser')
    except Exception as e:
        print("Error parsing HTML with BeautifulSoup:", e)
        return {}

    tokens_by_tag = {}
    pattern = re.compile(r'\b\w+\b')
    position_counter = 0

    for element in soup.find_all(True):
        tag_name = element.name.lower()
        text = element.get_text(strip=True)
        
        if text:
            tokens = word_tokenize(text)
            filtered_tokens = [token for token in tokens if pattern.match(token)]
            
            for token in filtered_tokens:
                stemmed_token = stemmer.stem(token.lower())
                if stemmed_token in tokens_by_tag:
                    tokens_by_tag[stemmed_token][0].append(tag_name)
                    tokens_by_tag[stemmed_token][1].append(position_counter)
                    tokens_by_tag[stemmed_token][2] += 1
                else:
                    tokens_by_tag[stemmed_token] = [[tag_name], [position_counter], 1]
                
                position_counter += 1

    return tokens_by_tag

def write_partial_index(index, doc_id):
    # Writes the partial index to disk
    partial_index_filename = f"index_part_{doc_id}.json"
    with open(partial_index_filename, "w") as outfile:
        json.dump(index, outfile)

def main():
    index_builder()
    # Following partial index creation, merge the partial indexes into a final index as needed
    data = Analyitics("index.json")
    document_count = data.get_document_count()
    token_count = data.get_token_count()
    index_size = data.get_index_size()
    with open("data_report.txt", "w") as report:
        report.write(f"Total Number of Indexed Documents: {document_count}\n\n")
        report.write(f"Total Number of Unique Tokens: {token_count}\n\n")
        report.write(f"Total Size of Index: {index_size}\n\n")

if __name__ == "__main__":
    nltk.download('punkt')
    main()
