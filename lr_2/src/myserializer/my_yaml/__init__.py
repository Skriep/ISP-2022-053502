from typing import TextIO
from myserializer.packer import Packer
from myserializer.serializer import Serializer
import yaml


class YamlSerializer(Serializer):
    def dump(self, obj, fp: TextIO):
        packed = Packer.pack(obj)
        yaml.safe_dump(packed, fp)

    def dumps(self, obj) -> str:
        packed = Packer.pack(obj)
        return yaml.safe_dump(packed)

    def load(self, fp: TextIO):
        return Packer.unpack(yaml.safe_load(fp))

    def loads(self, s: str):
        return Packer.unpack(yaml.safe_load(s))
