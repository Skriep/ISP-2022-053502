from serialization_inputs import test_inputs
from serialization_options import serializers
import pytest
import io


def dumps_loads(item, serializer):
    serialized = serializer.dumps(item)
    deserialized = serializer.loads(serialized)
    return deserialized


def dump_load(item, serializer):
    with io.StringIO() as serialization_stream:
        serializer.dump(item, serialization_stream)
        serialization_stream.flush()
        serialization_stream.seek(0)
        deserialized = serializer.load(serialization_stream)
    return deserialized


@pytest.mark.parametrize('test_input', test_inputs)
@pytest.mark.parametrize('serializer', serializers)
def test_serialization(test_input, serializer):
    assert dumps_loads(test_input, serializer) == test_input


@pytest.mark.parametrize('test_input', test_inputs)
@pytest.mark.parametrize('serializer', serializers)
def test_serialization_to_file(test_input, serializer):
    assert dump_load(test_input, serializer) == test_input
