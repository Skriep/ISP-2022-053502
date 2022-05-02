from typing import TextIO
from myserializer.packer import Packer
import toml


def dump(obj, fp: TextIO):
    packed = Packer.pack(obj)
    toml.dump(packed, fp)


def dumps(obj) -> str:
    packed = Packer.pack(obj)
    return toml.dumps(packed)


def load(fp: TextIO):
    return Packer.unpack(toml.load(fp))


def loads(s: str):
    return Packer.unpack(toml.loads(s))
