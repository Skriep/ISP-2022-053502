from typing import TextIO
from myserializer.packer import Packer
from myserializer.serializer import Serializer
import toml


class TomlSerializer(Serializer):
    def dump(self, obj, fp: TextIO):
        packed = Packer.pack(obj)
        toml.dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = Packer.pack(obj)
        return toml.dumps(packed)

    def load(self, fp: TextIO):
        return Packer.unpack(toml.load(fp))

    def loads(self, s: str):
        return Packer.unpack(toml.loads(s))
