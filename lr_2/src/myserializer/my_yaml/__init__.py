"""MyYAML module.

This module can serialize and deserialize objects to (from)
string or TextIO in YAML format.

If imported as module, the class YamlSerializer is available.
"""
from typing import Any, TextIO

import yaml
from myserializer.serializer import Serializer


class YamlSerializer(Serializer):
    """The class provides methods for object serialization.

    This class subclasses Serializer class.
    It implements object serialization in YAML format.
    """

    def dump(self, obj, fp: TextIO) -> None:
        """Serialize the object to TextIO in YAML format.

        Args:
            obj (object): object to be serialized.
            fp (TextIO): writable IO.
        """
        packed = self.packer.pack(obj)
        yaml.safe_dump(packed, fp)

    def dumps(self, obj) -> str:
        """Serialize the object to str in YAML format.

        Args:
            obj (object): object to be serialized.

        Returns:
            str: object serialized to str.
        """
        packed = self.packer.pack(obj)
        return yaml.safe_dump(packed)

    def load(self, fp: TextIO) -> Any:
        """Deserialize an object from TextIO in YAML format.

        Args:
            fp (TextIO): readable IO.

        Returns:
            deserialized object.
        """
        return self.packer.unpack(yaml.safe_load(fp))

    def loads(self, s: str) -> Any:
        """Deserialize an object from str in YAML format.

        Args:
            s (str): string representing serialized object.

        Returns:
            deserialized object.
        """
        return self.packer.unpack(yaml.safe_load(s))
