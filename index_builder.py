import os
import json
from bs4 import BeautifulSoup
from tokenizer import tokenize
from collections import defaultdict
from heapq import heappush, heappop
from itertools import groupby

def build_index(data_dir, stemmer):
    """
    Builds an inverted index from a set of JSON files containing web page data.
    
    Parameters:
    - data_dir (str): Path to the directory containing JSON files to be indexed.
    - stemmer (SnowballStemmer): Stemmer used to reduce words to their base form.
    
    Returns:
    - index (dict): Dictionary where each key is a token and the value is a ListOfPostings.
    - url_mapping (dict): Maps document IDs to URL information.
    """
    index = defaultdict(list)  # Stores tokens with associated postings
    url_mapping = {}  # Maps document ID to its URL and file metadata
    doc_id = 1  # Incremental document ID
    batch_size = 10000

    # Walk through the directory to process each JSON file
    for root, _, files in os.walk(data_dir):
        print("Currently building index with directory:", root)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", errors="ignore") as file:
                try:
                    data = json.load(file)  # Load JSON data from the file
                    url = data["url"]  # Extract URL
                    content = data["content"]  # Extract HTML content
                    
                    # Parse HTML content and extract visible text
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    
                    # Tokenize and stem words in the text
                    tokens = tokenize(text, stemmer)
                    token_counts = defaultdict(int)

                    # Count the frequency of each token in the document
                    for token in tokens:
                        token_counts[token] += 1
                    
                    # Add each token to the index with a posting entry
                    for token, frequency in token_counts.items():
                        index[token].append([doc_id, frequency])

                    if doc_id % batch_size == 0:
                        write_partial_index(index, doc_id)
                        index.clear()

                    # Store document metadata in the URL mapping
                    url_mapping[doc_id] = (url, file_name, len(tokens))
                    doc_id += 1  # Increment document ID for the next file
                except json.JSONDecodeError:
                    # Skip files that aren't properly formatted JSON
                    continue
    #return index, url_mapping

    # Write any remaining index and URL mappings
    write_partial_index(index, doc_id)  # Write any remaining index data
    write_url_mapping(url_mapping)
    
def write_partial_index(index, doc_id):
    # Writes the partial index to disk
    print(f"Writing partial_index {doc_id - 10000} - {doc_id}")
    partial_index_filename = f"partial_indexes/index_part_{doc_id}.json"
    with open(partial_index_filename, "w") as outfile:
        json.dump(index, outfile)

def write_url_mapping(url_mapping):
    with open("url_mapping.json", "w", encoding='utf-8') as file:
            json.dump(url_mapping, file)

def merge_partial_indexes_streaming(output_file="full_index.json"):
    """
    Merges all partial index JSON files in the 'partial_indexes' directory into a single full index JSON file
    without keeping the entire index in memory.

    Args:
        output_file (str): The name of the output file to write the merged index to.
    """
    # Directory containing the partial index files
    # Directory containing the partial index files
    partial_indexes_dir = "partial_indexes"

    # Collect all partial index filenames
    partial_files = [
        os.path.join(partial_indexes_dir, f)
        for f in os.listdir(partial_indexes_dir)
        if f.endswith(".json")
    ]

    # Open output file for writing
    with open(output_file, "w") as outfile:
        #outfile.write("{")  # Start JSON object
        first_entry = True  # Track whether it's the first entry in the JSON

        # Create a priority queue to merge tokens incrementally
        heap = []

        # Open all files and push their contents to the heap
        file_handles = []
        for filepath in partial_files:
            file_handle = open(filepath, "r")
            partial_index = json.load(file_handle)
            file_handles.append(file_handle)

            # Push each token to the heap with its source file
            for token, postings in partial_index.items():
                heappush(heap, (token, postings))

        # Merge tokens from the heap
        while heap:
            # Get the smallest token from the heap
            token, postings = heappop(heap)

            # Merge postings for the same token
            merged_postings = postings
            while heap and heap[0][0] == token:
                _, next_postings = heappop(heap)
                merged_postings.extend(next_postings)

            # Sort postings by document ID
            merged_postings = sorted(merged_postings, key=lambda x: x[0])

            # Write the token and postings to the output file
            if not first_entry:
                outfile.write(",")
            first_entry = False
            json.dump({token: merged_postings}, outfile)

        #outfile.write("}")  # Close JSON object

    # Close all open file handles
    for handle in file_handles:
        handle.close()
