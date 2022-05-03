from abc import ABC, abstractmethod
from typing import TextIO


class Serializer(ABC):
    @abstractmethod
    def dump(self, obj, fp: TextIO):
        pass

    @abstractmethod
    def dumps(self, obj) -> str:
        pass

    @abstractmethod
    def load(self, fp: TextIO):
        pass

    @abstractmethod
    def loads(self, s: str):
        pass
