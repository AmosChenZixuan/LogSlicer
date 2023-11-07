from .tokenizers import TikTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DLTBlockSplitter(RecursiveCharacterTextSplitter):
    def __init__(self, chunk_size, chunk_overlap = 0, length_func = TikTokenizer.get_token_count):
        super().__init__(
            separators = ["START"],
            # Set a really small chunk size, just to show.
            chunk_size = chunk_size,
            chunk_overlap  = chunk_overlap,
            length_function = length_func,
            is_separator_regex = True
        )

        