from abc import abstractmethod

class BaseMemory:
    @abstractmethod
    def store(self, object):
        pass

    @abstractmethod
    def retrieve(self, object):
        pass
