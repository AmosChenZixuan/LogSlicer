import time
from langchain.callbacks import get_openai_callback

from utils.templates import MappingTemplate, ReduceTemplate
from utils.models.llms import LLMFactory
from utils.preprocess import PreprocessorFactory
from chains import get_summarization_chain


def run_pipeline(filepath, log_type):
    # prepare docs
    preprocessor = PreprocessorFactory.create(filepath, log_type)
    chunks = preprocessor.run(chunk_size=6000)
    # prepare prompts
    map_prompt_template = MappingTemplate()
    reduce_prompt_template = ReduceTemplate() 
    # prepare llm
    llm = LLMFactory.create('azure')

    start_time = time.time()
    with get_openai_callback() as callback:
        summary_chain = get_summarization_chain(llm=llm,
                            map_prompt=map_prompt_template,
                            reduce_prompt=reduce_prompt_template,
                            verbose=True)
        
        output = summary_chain.run(chunks)
    elapsed_t = round(time.time() - start_time)
    return {
        'report': output,
        'callback': str(callback),
        'chunks': len(chunks),
        'time': elapsed_t
    }

def run_fake_pipeline():
    return {
        'report': '##Testing',
        'callback': '',
        'chunks': 0,
        'time': 0
    }