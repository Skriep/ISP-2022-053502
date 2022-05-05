"""MyTOML module.

This module can serialize and deserialize objects to (from)
string or TextIO in TOML format.

If imported as module, the class TomlSerializer is available.
"""
from typing import Any, TextIO

import toml
from myserializer.serializer import Serializer


class TomlSerializer(Serializer):
    """The class provides methods for object serialization.

    This class subclasses Serializer class.
    It implements object serialization in TOML format.
    """

    def dump(self, obj, fp: TextIO) -> None:
        """Serialize the object to TextIO in TOML format.

        Args:
            obj (object): object to be serialized.
            fp (TextIO): writable IO.
        """
        packed = self.packer.pack(obj)
        toml.dump(packed, fp)

    def dumps(self, obj) -> str:
        """Serialize the object to str in TOML format.

        Args:
            obj (object): object to be serialized.

        Returns:
            str: object serialized to str.
        """
        packed = self.packer.pack(obj)
        return toml.dumps(packed)

    def load(self, fp: TextIO) -> Any:
        """Deserialize an object from TextIO in TOML format.

        Args:
            fp (TextIO): readable IO.

        Returns:
            deserialized object.
        """
        return self.packer.unpack(toml.load(fp))

    def loads(self, s: str) -> Any:
        """Deserialize an object from str in TOML format.

        Args:
            s (str): string representing serialized object.

        Returns:
            deserialized object.
        """
        return self.packer.unpack(toml.loads(s))
