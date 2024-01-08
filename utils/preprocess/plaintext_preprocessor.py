from .base_preprocessor import BasePreprocessor

from utils.dlt.text_splitters import DLTBlockSplitter

class PlaintextPreprocessor(BasePreprocessor):
    def extract_documents(self, filename):
        with open(filename, 'r') as f:
            documents = f.readlines()
        return documents

    def chunk_documents(self, documents, chunk_size):
        text_splitter = DLTBlockSplitter(chunk_size)
        chunks = text_splitter.create_documents([''.join(documents)])

        return chunks