from abc import ABC, abstractmethod


class Loder(ABC):
    def __init__(self):
        self.data: list[dict] = []

    @abstractmethod
    def load(self, file) -> list[dict]:
        pass
