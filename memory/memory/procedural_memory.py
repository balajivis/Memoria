from memory.base_memory import BaseMemory


class ProceduralMemory(BaseMemory):
    def __init__(self):
        self.functions = []

    def store(self, kv):
        key, description = kv
        self.functions((key, description))

    def retrieve(self, obj):
        return self.functions