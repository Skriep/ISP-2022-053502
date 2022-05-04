from myserializer.serializer import Serializer
from serialization_inputs import test_inputs, test_funcs_with_args
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


@pytest.mark.parametrize('test_input', [
    '"just a string"', '["array", 1, 2]', '{"f" : "f"}'
])
@pytest.mark.parametrize('serializer', serializers)
def test_not_unpackable(test_input, serializer):
    with pytest.raises(Exception):
        serializer.loads(test_input)


@pytest.mark.parametrize('test_func,test_args', test_funcs_with_args)
@pytest.mark.parametrize('serializer', serializers)
@pytest.mark.parametrize('cycle_serialization', [dumps_loads, dump_load])
def test_function_serialization(test_func, test_args, serializer: Serializer,
                                cycle_serialization):
    serializer.globals = test_func.__globals__
    acquired_func = cycle_serialization(test_func, serializer)
    serializer.globals = None
    assert acquired_func.__doc__ == test_func.__doc__
    for test_arg in test_args:
        assert acquired_func(*test_arg) == test_func(*test_arg)
