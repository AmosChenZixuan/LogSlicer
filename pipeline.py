from langchain.callbacks import get_openai_callback

from preprocess import create_documents, chunk_documents
from utils.templates import SystemPromptMappingTemplate, SystemPromptConbineTemplate
from models.llms import LLMFactory
from chains import get_summarization_chain


def run_pipeline(filepath):
    # prepare docs
    documents = create_documents("logs/dlt/HPA_partnumber not updated.dlt")
    chunks = chunk_documents(documents, chunk_size=200)
    print(len(chunks))
    # prepare prompts
    map_prompt_template = SystemPromptMappingTemplate()
    combine_prompt_template = SystemPromptConbineTemplate() 
    # prepare llm
    llm = LLMFactory.create('azure', engine='gpt-4')

    with get_openai_callback() as callback:
        summary_chain = get_summarization_chain(llm=llm,
                            map_prompt=map_prompt_template,
                            reduce_prompt=combine_prompt_template,
                            verbose=True)
        
        output = summary_chain.run(chunks[:3])
    return {
        'report': output,
        'callback': str(callback)
    }