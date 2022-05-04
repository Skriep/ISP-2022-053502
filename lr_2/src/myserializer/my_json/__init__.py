"""MyJSON module.

This module can serialize and deserialize objects to (from)
string or TextIO in JSON format.

If imported as module, the class JsonSerializer is available.
"""
from typing import TextIO, Any, cast
from myserializer.my_json.encoder import JsonEncoder
from myserializer.my_json.decoder import JsonDecoder
import io
from myserializer.serializer import Serializer


class JsonSerializer(Serializer):
    """The class provides methods for object serialization.

    This class subclasses Serializer class.
    It implements object serialization in JSON format.
    """

    def dump(self, obj, fp: TextIO) -> None:
        """Serialize the object to TextIO in JSON format.

        Args:
            obj (object): object to be serialized.
            fp (TextIO): writable IO.
        """
        packed = self.packer.pack(obj)
        encoder = JsonEncoder()
        fp.write(encoder.encode(packed))

    def dumps(self, obj) -> str:
        """Serialize the object to str in JSON format.

        Args:
            obj (object): object to be serialized.

        Returns:
            str: object serialized to str.
        """
        with io.StringIO() as stream:
            self.dump(obj, stream)
            return stream.getvalue()

    def load(self, fp: TextIO) -> Any:
        """Deserialize an object from TextIO in JSON format.

        Args:
            fp (TextIO): readable IO.

        Returns:
            deserialized object.
        """
        decoder = JsonDecoder()
        decoded = decoder.decode(fp)
        if type(decoded) is not dict:
            raise ValueError('Decoded value cannot be unpacked')
        decoded = cast(dict, decoded)
        return self.packer.unpack(decoded)

    def loads(self, s: str) -> Any:
        """Deserialize an object from str in JSON format.

        Args:
            s (str): string representing serialized object.

        Returns:
            deserialized object.
        """
        with io.StringIO(s) as stream:
            return self.load(stream)
