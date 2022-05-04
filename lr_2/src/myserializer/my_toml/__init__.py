from typing import TextIO
from myserializer.packer import Packer
from myserializer.serializer import Serializer
from typing import Any
import toml


class TomlSerializer(Serializer):
    def dump(self, obj, fp: TextIO) -> None:
        packed = Packer.pack(obj)
        toml.dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = Packer.pack(obj)
        return toml.dumps(packed)

    def load(self, fp: TextIO) -> Any:
        return Packer.unpack(toml.load(fp), self.globals)

    def loads(self, s: str) -> Any:
        return Packer.unpack(toml.loads(s), self.globals)
