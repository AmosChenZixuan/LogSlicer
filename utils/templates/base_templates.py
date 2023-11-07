import textwrap
class BaseStrTemplate:
    def __init__(self, template, **kargs):
        self._text = textwrap.dedent(template).strip()
        if len(kargs) > 0:
            self._text = self._text.format(**kargs)
    
    
    def __repr__(self):
        return self._text
