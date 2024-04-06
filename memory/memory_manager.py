from memory.associative_memory import AssociativeMemory
from memory.longterm_memory import LongtermSummaryMemory
from memory.procedural_memory import ProceduralMemory
from memory.working_memory import WorkingMemory


class MemoryManager:
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.associative_memory = AssociativeMemory()
        self.longterm_memory = LongtermSummaryMemory()
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

    # Example of storing and retrieving data
    memory_manager.store('procedural',
                         'Hackathon', "Setup the Git hub repo")
    print(memory_manager.retrieve('procedural', 'Hackathon'))
