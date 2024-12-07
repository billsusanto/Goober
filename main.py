<<<<<<< HEAD
import os
from index_builder import build_index, save_index_to_file
from analytics import generate_analytics_report
from nltk.stem import SnowballStemmer
import json
=======
from index_builder import build_index, postprocess_index
from analytics import generate_analytics_report
from nltk.stem import SnowballStemmer
>>>>>>> daniel

if __name__ == "__main__":
      # Define paths for data and output files
      data_dir = "./DEV"  # Directory containing files to index

      # Initialize a stemmer for token processing
      stemmer = SnowballStemmer("english")

<<<<<<< HEAD
      # Build the index and URL mapping from the provided data directory
      print("Building index...")
      index, url_mapping = build_index(data_dir, stemmer)
      with open("./indices/dev_index.json", "w") as outfile:
            json.dump(index, outfile)

      # Save URL mappings to a separate 
      ### json instead of txt
      with open("url_mapping.json", "w", encoding='utf-8') as file:
            json.dump(url_mapping, file)

      # Generate a report with basic analytics on the index
      generate_analytics_report("./indices/dev_index.json", "url_mapping.json")
=======

      # Build the index and URL mapping from the provided data directory
      print("Building index...")
      build_index(data_dir, stemmer)
      postprocess_index() # postprocess turns partial indexes folder into final indicies folder
                          # final index 0 contains index with only tagged terms
                          # the rest (1-6) are just alphabetical buckets with ONLY frequency, no 
                          # when querying we'll only search indicies 1-6 as a last resort.


      # Generate a report with basic analytics on the index
      generate_analytics_report("./partial_indexes", "url_mapping.json")
>>>>>>> daniel
