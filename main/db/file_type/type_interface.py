from abc import ABC, abstractmethod


class Loder(ABC):
    def __init__(self):
        self.data = []

    @abstractmethod
    def load(self, file) -> object:
        pass
