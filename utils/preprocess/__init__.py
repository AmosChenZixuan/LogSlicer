from .plaintext_preprocessor import PlaintextPreprocessor
from .dlt_preprocessor import DLTPreprocessor

class PreprocessorFactory:
    @staticmethod
    def create(filepath, log_type):
        if log_type == 'plain_text':
            return PlaintextPreprocessor(filepath)
        elif log_type == 'dlt':
            return DLTPreprocessor(filepath)
        else:
            raise ValueError(f'Unknown log type: {log_type}')