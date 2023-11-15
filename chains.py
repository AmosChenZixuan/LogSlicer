from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain


def get_map_reduce_chain(llm, map_prompt, reduce_prompt, verbose=False):
    # https://python.langchain.com/docs/use_cases/summarization

    map_chain = LLMChain(llm=llm,
                         prompt=map_prompt,
                         verbose=verbose)
    reduce_chain = LLMChain(llm=llm,
                            prompt=reduce_prompt,
                            verbose=verbose)
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain,
        document_variable_name="text",
        verbose=verbose
    )
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
        verbose=verbose
    )
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="text",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
        verbose=verbose
    )
    return map_reduce_chain

def get_summarization_chain(llm, map_prompt, reduce_prompt, verbose=False):
    summary_chain = load_summarize_chain(llm=llm,
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt,
                                     combine_prompt=reduce_prompt,
                                     verbose=verbose)
    return summary_chain