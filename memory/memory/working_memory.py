from memory.base_memory import BaseMemory


class WorkingMemory(BaseMemory):
    def __init__(self):
        # Initialize the internal storage as a dictionary
        self.memory = {}

    def store(self, key, value):
        """
        Store or update the value in the working memory associated with the key.

        :param key: The identifier for the data to be stored or updated.
        :param value: The data to be stored or the new value for updating an existing entry.
        """
        self.memory[key] = value

    def retrieve(self, key):
        """
        Retrieve the value from the working memory associated with the key.

        :param key: The identifier for the data to be retrieved.
        :return: The data associated with the key, or None if the key does not exist.
        """
        return self.memory.get(key)

    def clear_memory(self):
        """
        Clears all the data stored in the working memory.
        """
        self.memory.clear()
