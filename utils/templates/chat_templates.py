
from .base_templates import BaseStrTemplate

class SystemPromptMappingTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        self.template = '''\
        You are a senior software engineer. Your task is to summarize logs. The logs given to you are divided into blocks following this format:
        {log_format}
        You should point out things that are causing errors. You should also provide suggestions or solutions if there are any. You are very
        detailed and thorough looking at errors and best practices. The summary should be short and to the point.
        '''
        super().__init__(self.template, **kargs)


class SystemPromptReductionTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        self.template = '''\
        You are a senior software engineer. Your task is to summarize logs. Given the following summaries of different parts of the same log, 
        combine and refine them into a unified summary. The summary output should be in well formatted Markdown in a text window and the column width of the output 
        should be max 100 characters.
        {summaries}
        '''
        super().__init__(self.template, **kargs)
