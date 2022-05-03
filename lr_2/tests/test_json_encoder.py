from encoding_inputs import test_inputs
from myserializer.my_json.encoder import JsonEncoder
import pytest
import json


def encode_loads(obj, encoder: JsonEncoder):
    return json.loads(encoder.encode(obj))


@pytest.mark.parametrize('test_input', test_inputs)
def test_compatibility(test_input):
    encoder = JsonEncoder()
    print(encode_loads(test_input, encoder))
    assert encode_loads(test_input, encoder) == test_input
