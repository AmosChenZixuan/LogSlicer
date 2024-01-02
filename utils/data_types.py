from .text_transformers import sub_hex_numeric, sub_perf_counter

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
    

class DLTPayload(str):
    def replace_hex_and_numeric(self, rep='MASK'):
        return DLTPayload(sub_hex_numeric(self, rep))
    
    def replace_value_before_time_unit(self, rep='MASK'):
        return DLTPayload(sub_perf_counter(self, rep))
    
    def set_dlt_index(self, index):
        self.dlt_index = index
        return self
    
    def set_msg_type(self, type):
        self.msg_type = type
        return self