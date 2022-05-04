from typing import TextIO
from myserializer.serializer import Serializer
from typing import Any
import toml


class TomlSerializer(Serializer):
    def dump(self, obj, fp: TextIO) -> None:
        packed = self.packer.pack(obj)
        toml.dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = self.packer.pack(obj)
        return toml.dumps(packed)

    def load(self, fp: TextIO) -> Any:
        return self.packer.unpack(toml.load(fp))

    def loads(self, s: str) -> Any:
        return self.packer.unpack(toml.loads(s))
