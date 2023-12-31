from .base_templates import BaseStrTemplate

class SessionBlockTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        _template = '''\
        START {title}
        {content}
        END
        '''
        super().__init__(_template, input_variables = ['title', 'content'], **kargs)

class SessionLineTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        _template = '''\
        [{index}] {count} {type}: {payload}
        '''
        super().__init__(_template, input_variables = ['index', 'count', 'type', 'payload'], **kargs)