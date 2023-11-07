from .base_templates import BaseStrTemplate

class SessionBlockTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        self.template = '''\
        START {title} {num_sessions}
        {content}
        END
        '''
        super().__init__(self.template, **kargs)

class SessionLineTemplate(BaseStrTemplate):
    def __init__(self, **kargs):
        self.template = '''\
        {count}: {payload}
        '''
        super().__init__(self.template, **kargs)