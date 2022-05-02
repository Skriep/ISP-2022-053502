from typing import TextIO
from myserializer.packer import Packer
import yaml


def dump(obj, fp: TextIO):
    packed = Packer.pack(obj)
    yaml.safe_dump(packed, fp)


def dumps(obj) -> str:
    packed = Packer.pack(obj)
    return yaml.safe_dump(packed)


def load(fp: TextIO):
    return Packer.unpack(yaml.safe_load(fp))


def loads(s: str):
    return Packer.unpack(yaml.safe_load(s))
