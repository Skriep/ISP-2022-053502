"""Serializer module.

This module defines an abstract class Serializer.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, TextIO

from myserializer.packer import Packer


class Serializer(ABC):
    """The class provides abstract methods for object serialization.

    Provided methods:
    - dump - serialize object to TextIO;
    - dumps - serialize object to string;
    - load - deserialize object from TextIO;
    - loads - deserialize object from string.

    Note:
        Objects serialized using Python of some version
        must be deserialized using that specific version of Python.
    """

    _globals = None

    def __init__(self, globals: Dict[str, Any] = None) -> None:
        """__init__ method.

        Args:
            globals (dict, optional): value for globals property.
        """
        self._globals = globals
        self.packer = Packer(self.globals)

    @property
    def globals(self) -> 'Dict[str, Any] | None':
        """Get or set globals value.

        globals is used on deserialization of functions:
        it replaces deserialized function's __globals__ attribute.

        The dictionary must contain all the necessary global variables
        required to execute the function.

        If functions are not being deserialized, changing the value of globals
        has no effect.
        """
        return self._globals

    @globals.setter
    def globals(self, value: 'Dict[str, Any] | None'):
        self._globals = value
        self.packer.globals = self._globals

    @abstractmethod
    def dump(self, obj, fp: TextIO) -> None:
        """Serialize object to TextIO."""

    @abstractmethod
    def dumps(self, obj) -> str:
        """Serialize the object to str."""

    @abstractmethod
    def load(self, fp: TextIO) -> Any:
        """Deserialize an object from TextIO."""

    @abstractmethod
    def loads(self, s: str) -> Any:
        """Deserialize an object from str."""
