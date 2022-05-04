from typing import TextIO
from myserializer.packer import Packer
from myserializer.serializer import Serializer
from typing import Any
import yaml


class YamlSerializer(Serializer):
    def dump(self, obj, fp: TextIO) -> None:
        packed = Packer.pack(obj)
        yaml.safe_dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = Packer.pack(obj)
        return yaml.safe_dump(packed)

    def load(self, fp: TextIO) -> Any:
        return Packer.unpack(yaml.safe_load(fp), self.globals)

    def loads(self, s: str) -> Any:
        return Packer.unpack(yaml.safe_load(s), self.globals)
