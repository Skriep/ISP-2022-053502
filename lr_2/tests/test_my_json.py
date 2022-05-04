"""my_json tests.

This module provides a number of tests to be used by PyTest.
It targets testing myserializer.my_json module:
- Checking if my_json output is compatible with json;
- Checking if json output can be decoded by my_json;
- Checking is my_json can work with custom separators.
"""
from encoding_inputs import test_inputs
from myserializer.my_json.encoder import JsonEncoder
from myserializer.my_json.decoder import JsonDecoder
import pytest
import json


def encode_loads(obj, encoder: JsonEncoder):
    """encode_loads function.

    Calls encoder.encode(obj), saves the result
    and returns json.loads(result).
    """
    return json.loads(encoder.encode(obj))


def dumps_decode(obj, decoder: JsonDecoder):
    """dumps_decode function.

    Calls json.dumps(obj), saves the result
    and returns decoder.decode(result).
    """
    return decoder.decode(json.dumps(obj))


def encode_decode(obj, encoder: JsonEncoder, decoder: JsonDecoder):
    """encode_decode function.

    Calls encoder.encode(obj), saves the result
    and returns decoder.decode(result).
    """
    return decoder.decode(encoder.encode(obj))


@pytest.mark.parametrize('test_input', test_inputs)
def test_encoding(test_input):
    """test_encoding function.

    Tests JsonEncoder by calling encode_loads
    and comparing its result with test_input.
    """
    encoder = JsonEncoder()
    assert encode_loads(test_input, encoder) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
def test_decoding(test_input):
    """test_decoding function.

    Tests JsonDecoder by calling dumps_decode
    and comparing its result with test_input.
    """
    decoder = JsonDecoder()
    assert dumps_decode(test_input, decoder) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
@pytest.mark.parametrize('test_separators', [
    ('.', '+'), ('/', ')'), ('m', 'b')
])
def test_encoding_separators(test_input, test_separators):
    """test_encoding_separators function.

    Tests both JsonEncoder and JsonDecoder
    (both initialized with separators=test_separators)
    by calling encode_decode and comparing its result with test_input.

    It is expected for those values to be equal.
    """
    encoder = JsonEncoder(separators=test_separators)
    decoder = JsonDecoder(separators=test_separators)
    assert encode_decode(test_input, encoder, decoder) == test_input


@pytest.mark.parametrize('test_separators', [
    ('ae fae ', ''), (' ', '    '), ('\r\n', '')
])
def test_invalid_separators(test_separators):
    """test_invalid_separators function.

    Tests JsonDecoder (initialized with separators=test_separators).

    It is expected for separators to be invalid.
    JsonDecoder is expected to raise ValueError on initialization.
    """
    with pytest.raises(ValueError):
        JsonDecoder(separators=test_separators)
