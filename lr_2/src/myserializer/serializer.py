from abc import ABC, abstractmethod
from typing import Any, Dict, TextIO

from myserializer.packer import Packer


class Serializer(ABC):
    _globals = None

    def __init__(self, globals: Dict[str, Any] = None) -> None:
        self._globals = globals
        self.packer = Packer(self.globals)

    def set_globals(self, globals: 'Dict[str, Any] | None'):
        self._globals = globals
        self.packer.globals = self._globals

    def get_globals(self) -> 'Dict[str, Any] | None':
        return self._globals

    globals = property(get_globals, set_globals)

    @abstractmethod
    def dump(self, obj, fp: TextIO) -> None: pass

    @abstractmethod
    def dumps(self, obj) -> str: pass

    @abstractmethod
    def load(self, fp: TextIO) -> Any: pass

    @abstractmethod
    def loads(self, s: str) -> Any: pass
