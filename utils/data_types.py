class NestedDefaultdict(dict):
    def __init__(self, factory_func, depth, *args, **kwargs):
        self._factory_func = factory_func
        self._depth = depth
        super().__init__(*args, **kwargs)
    
    def __missing__(self, key):
        if self._depth > 1:
            self[key] = NestedDefaultdict(self._factory_func, self._depth - 1)
        else:
            self[key] = self._factory_func() 
        return self[key]