from typing import TextIO
from myserializer.serializer import Serializer
from typing import Any
import yaml


class YamlSerializer(Serializer):
    def dump(self, obj, fp: TextIO) -> None:
        packed = self.packer.pack(obj)
        yaml.safe_dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = self.packer.pack(obj)
        return yaml.safe_dump(packed)

    def load(self, fp: TextIO) -> Any:
        return self.packer.unpack(yaml.safe_load(fp))

    def loads(self, s: str) -> Any:
        return self.packer.unpack(yaml.safe_load(s))
