from myserializer.packer import Packer
import pytest
from serialization_inputs import test_inputs


def pack_unpack(item, packer):
    packed = packer.pack(item)
    unpacked = packer.unpack(packed)
    return unpacked


@pytest.mark.parametrize('test_input', test_inputs)
def test_packing(test_input):
    packer = Packer()
    assert pack_unpack(test_input, packer) == test_input
