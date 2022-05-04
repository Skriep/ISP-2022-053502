"""my_json tests.

This module provides a number of tests to be used by PyTest.
It targets testing myserializer.packer module:
- Checking if object after being repacked does not change type and value.
"""
from myserializer.packer import Packer
import pytest
from serialization_inputs import test_basic


def pack_unpack(item, packer: Packer):
    """pack_unpack function.

    First calls packer.pack(item), saves the result and
    returns packer.unpack(result).
    """
    packed = packer.pack(item)
    unpacked = packer.unpack(packed)
    return unpacked


@pytest.mark.parametrize('test_input', test_basic)
def test_packing(test_input):
    """test_packing function.

    Checks that an object after pack_unpack does not change:
    - type;
    - value.

    Preservation of value is checked by performing a comparison (==)
    of repacked value and test_input.
    """
    packer = Packer()
    repacked = pack_unpack(test_input, packer)
    assert type(repacked) == type(test_input)
    assert repacked == test_input
