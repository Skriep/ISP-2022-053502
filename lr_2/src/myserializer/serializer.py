from abc import ABC, abstractmethod
from typing import Any, Dict, TextIO


class Serializer(ABC):
    def __init__(self, globals: Dict[str, Any] = None) -> None:
        self.globals = globals

    @abstractmethod
    def dump(self, obj, fp: TextIO) -> None:
        pass

    @abstractmethod
    def dumps(self, obj) -> str:
        pass

    @abstractmethod
    def load(self, fp: TextIO) -> Any:
        pass

    @abstractmethod
    def loads(self, s: str) -> Any:
        pass
