#Maybe class is not necessary but we need to somehow collect:
#The number of indexed documents;
#The number of unique tokens;
#The total size (in KB) of your index on disk.
import os


class Analyitics:
    def __init__(self, index_file):
        self._document_count = 0
        self._token_count = 0
        self._index_size = 0
        self.set_document_count()
        self.set_token_count(index_file)
        self.set_index_size(index_file)

    def set_document_count(self):
        with open("url_mapping.txt", "r") as mapping:
            for lines in mapping:
                self._document_count += 1

    def set_token_count(self, index_file):
        with open(index_file, "r") as index:
            for key in index:
                self._token_count += 1

    def set_index_size(self, index_file):
        file_size = os.path.getsize(index_file)
        file_size / 1024
        self._index_size = file_size

    def get_document_count(self):
        return self._document_count

    def get_token_count(self):
        return self._token_count
    
    def get_index_size(self):
        return self._index_size
        
        # to get size of file : file_size = os.path.getsize(file_path)