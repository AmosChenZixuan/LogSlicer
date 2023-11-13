import textwrap

from langchain.prompts import PromptTemplate

class BaseStrTemplate(PromptTemplate):
    def __init__(self, template, **kargs):
        template = textwrap.dedent(template).strip()

        super().__init__(template=template, **kargs)
