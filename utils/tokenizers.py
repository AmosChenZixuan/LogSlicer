import os
import tiktoken

from dotenv import load_dotenv
load_dotenv()

class TikTokenizer:
    tokenizer = None

    @staticmethod
    def get_tokenizer():
        if __class__.tokenizer is None:
            __class__.tokenizer = tiktoken.encoding_for_model(os.getenv("GPT_MODEL"))
        return __class__.tokenizer

    @staticmethod
    def get_token_count(text):
        tokenizer = __class__.get_tokenizer()
        text_token_count = len(tokenizer.encode(text))
        return text_token_count