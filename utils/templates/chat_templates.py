
from .base_templates import BaseStrTemplate

class SystemPromptMappingTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        _template = '''\
        You are a senior software engineer. Your task is to summarize logs. The logs given to you are divided into sessions following this format:
        START [session title]
        [occurrence count] [log type]: [payload]
        END
        Some numbers are replcaed with 'MASK' becasue they are not important.
        Log to be summarized: {{{text}}}
        Draft the summary following these steps:
        1. Read and understand the relation among the occurrence count, log type and the payload.
        2. Point out the important errors in the log.
        3. Identify potential root causes of the errors.
        4. Provide suggestions if there are any. 
        5. Organize information and write a concise summary.
        6. Revise to remove any redundant, inaacurate or vague information.
        Summary:
        '''
        super().__init__(_template, input_variables = ['text'], **kargs)


class SystemPromptConbineTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        _template = '''\
        You are a senior software engineer. Your task is to summarize logs. Given the following summaries of different parts of the same log, 
        combine and refine them into a concise summary. 
        Provided summaryies: {{{text}}}
        Draft the summary following these steps:
        1. Identify common points among the summaries. These will be the backbone of the final summary.
        2. Point out unique information in each summary. These could be important details.
        3. Organize information and write a concise summary. It should have one section for summary and one section for suggestions.
        4. Revise to remove any redundant, inaacurate or vague information.
        5. Write the final summary in formatted Markdown, ensuring the text width does not exceed 100 characters. Use bullet points for content organization
        Assume the output will be written into a markdown file.
        Final Summary:
        '''
        super().__init__(_template, input_variables = ['text'], **kargs)
