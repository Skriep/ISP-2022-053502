from encoding_inputs import test_inputs
from myserializer.my_json.encoder import JsonEncoder
from myserializer.my_json.decoder import JsonDecoder
import pytest
import json


def encode_loads(obj, encoder: JsonEncoder):
    return json.loads(encoder.encode(obj))


def dumps_decode(obj, decoder: JsonDecoder):
    return decoder.decode(json.dumps(obj))


def encode_decode(obj, encoder: JsonEncoder, decoder: JsonDecoder):
    return decoder.decode(encoder.encode(obj))


@pytest.mark.parametrize('test_input', test_inputs)
def test_encoding(test_input):
    encoder = JsonEncoder()
    assert encode_loads(test_input, encoder) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
def test_decoding(test_input):
    decoder = JsonDecoder()
    assert dumps_decode(test_input, decoder) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
@pytest.mark.parametrize('test_separators', [
    ('.', '+'), ('/', ')'), ('m', 'b')
])
def test_encoding_separators(test_input, test_separators):
    encoder = JsonEncoder(separators=test_separators)
    decoder = JsonDecoder(separators=test_separators)
    assert encode_decode(test_input, encoder, decoder) == test_input


@pytest.mark.parametrize('test_separators', [
    ('ae fae ', ''), (' ', '    '), ('\r\n', '')
])
def test_invalid_separators(test_separators):
    with pytest.raises(ValueError):
        JsonDecoder(separators=test_separators)
