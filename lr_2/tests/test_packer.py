from myserializer.packer import Packer
import pytest


def pack_unpack(item):
    packed = Packer.pack(item)
    unpacked = Packer.unpack(packed)
    return unpacked


@pytest.mark.parametrize('test_input', [
    1, 2, 12, 13434, -134134, 0, 7,
    True, False, (False, True), [True, (1, 2, 'k9')],
    {1: 2}, {'a': 'b'}, {None: 'ok'},
    {'key': 'value', 123: 456, 12.3: 4.56, (1.4j + 3): "that's complex!",
     (1, 2, 3): (4, 5, 6)},
    {'deep': {'deep': {'deep': {'deep': {'deep': {'deep': {'deep': 1}}}}}}},
    {1, 2, 3, 'this is SET', True, 13.4},
    frozenset({1, 2, '3', False, 3.14}),
    range(100), range(0, 1, 2), range(25, -10, -1),
    b'\x00\x01\x02 abc 123 \n\r -- \x93', b'123', b'bytes',
    bytearray(b'123'), bytearray((1, 2, 5, 3, 2, 6, 235, 12, 123))
])
def test_packing(test_input):
    assert pack_unpack(test_input) == test_input
