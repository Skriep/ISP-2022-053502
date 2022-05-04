from typing import TextIO, Any, cast
from myserializer.my_json.encoder import JsonEncoder
from myserializer.my_json.decoder import JsonDecoder
from myserializer.packer import Packer
import io
from myserializer.serializer import Serializer


class JsonSerializer(Serializer):
    def dump(self, obj, fp: TextIO) -> None:
        packed = Packer.pack(obj)
        encoder = JsonEncoder()
        fp.write(encoder.encode(packed))

    def dumps(self, obj) -> str:
        with io.StringIO() as stream:
            self.dump(obj, stream)
            return stream.getvalue()

    def load(self, fp: TextIO) -> Any:
        decoder = JsonDecoder()
        decoded = decoder.decode(fp)
        if type(decoded) is not dict:
            raise ValueError('Decoded value cannot be unpacked')
        decoded = cast(dict, decoded)
        return Packer.unpack(decoded, self.globals)

    def loads(self, s: str) -> Any:
        with io.StringIO(s) as stream:
            return self.load(stream)
