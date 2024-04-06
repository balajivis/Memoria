from memory.associative_memory import AssociativeMemory
from memory.longterm_memory import LongtermMemory
from memory.procedural_memory import ProceduralMemory
from memory.working_memory import WorkingMemory


class MemoryManager:
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.associative_memory = AssociativeMemory()
        self.longterm_memory = LongtermMemory()
        self.procedural_memory = ProceduralMemory()

    def store(self, memory_type, key, value):
        # Route store requests to the appropriate memory type
        getattr(self, f"{memory_type}_memory").store(key, value)

    def retrieve(self, memory_type, key):
        # Route retrieve requests to the appropriate memory type
        return getattr(self, f"{memory_type}_memory").retrieve(key)


# Example usage:
if __name__ == "__main__":
    memory_manager = MemoryManager()
    memory_manager.setup_databases()

    # Example of storing and retrieving data
    memory_manager.store('working', 'user_goal', 'Finish hackathon project')
    print(memory_manager.retrieve('working', 'user_goal'))
