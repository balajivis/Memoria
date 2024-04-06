from memory.base_memory import BaseMemory


class WorkingMemory(BaseMemory):
    def __init__(self):
        self.mem = {}

    '''
    object is a (key, value)
    '''
    @abstractmethod
    def store(self, kv):
        key, value = kv 
        self.mem[key] = value

    @abstractmethod
    def retrieve(self, key):
        return self.mem[key] 