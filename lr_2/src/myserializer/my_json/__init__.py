from typing import TextIO
from myserializer.my_json.encoder import JsonEncoder
from myserializer.packer import Packer
import io


def dump(obj, fp: TextIO):
    packed = Packer.pack(obj)
    encoder = JsonEncoder()
    fp.write(encoder.encode(packed))


def dumps(obj) -> str:
    with io.StringIO() as stream:
        dump(obj, stream)
        return stream.getvalue()


def load(fp: TextIO):
    # TODO
    pass


def loads(s: str):
    with io.StringIO(s) as stream:
        return load(stream)
