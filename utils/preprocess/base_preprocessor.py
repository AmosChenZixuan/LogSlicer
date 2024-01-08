from abc import ABC, abstractmethod

class BasePreprocessor(ABC):
    def __init__(self, filename):
        self.filename = filename

    def run(self, chunk_size):
        documents = self.extract_documents(self.filename)
        return self.chunk_documents(documents, chunk_size)

    @abstractmethod
    def extract_documents(self, filename):
        pass 

    @abstractmethod
    def chunk_documents(self, documents, chunk_size):
        pass