from myserializer.packer import Packer
import pytest
from serialization_inputs import test_inputs


def pack_unpack(item):
    packed = Packer.pack(item)
    unpacked = Packer.unpack(packed)
    return unpacked


@pytest.mark.parametrize('test_input', test_inputs)
def test_packing(test_input):
    assert pack_unpack(test_input) == test_input