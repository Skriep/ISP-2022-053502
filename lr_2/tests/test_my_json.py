from encoding_inputs import test_inputs
from myserializer.my_json.encoder import JsonEncoder
from myserializer.my_json.decoder import JsonDecoder
import pytest
import json


def encode_loads(obj, encoder: JsonEncoder):
    return json.loads(encoder.encode(obj))


def dumps_decode(obj, decoder: JsonDecoder):
    return decoder.decode(json.dumps(obj))


@pytest.mark.parametrize('test_input', test_inputs)
def test_encoding(test_input):
    encoder = JsonEncoder()
    assert encode_loads(test_input, encoder) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
def test_decoding(test_input):
    decoder = JsonDecoder()
    assert dumps_decode(test_input, decoder) == test_input
