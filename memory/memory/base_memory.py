from abc import ABC, abstractmethod


class BaseMemory(ABC):
    @abstractmethod
    def store(self, key, value):
        """
        Store or update the value in memory associated with the key.

        If the key already exists, the value will be updated.
        If the key does not exist, a new entry will be created.

        :param key: The identifier for the data to be stored or updated.
        :param value: The data to be stored or the new value for updating an existing entry.
        """
        pass

    @abstractmethod
    def retrieve(self, key):
        """
        Retrieve the value from memory associated with the key.

        :param key: The identifier for the data to be retrieved.
        :return: The data associated with the key.
        """
        pass
