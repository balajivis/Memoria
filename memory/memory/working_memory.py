from memory.base_memory import BaseMemory


class WorkingMemory(BaseMemory):
    def __init__(self):
        self.mem = {}

    '''
    object is a (key, value)
    '''
    def store(self, kv):
        key, value = kv 
        self.mem[key] = value

    def retrieve(self, key):
        return self.mem[key] 

    def modify(self, kv) -> bool:
        key, value = kv
        if key in self.mem:
            self.mem = value
            return True
    
        return False
