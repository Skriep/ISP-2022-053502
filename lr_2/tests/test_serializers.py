"""Serializer tests.

This module provides a number of tests to be used by PyTest.
It targets testing myserializer.serializer.Serializer:
- Checking if basic types (str, int, bool, etc.) can be correctly
serialized and deserialized;
- Checking if user-defined functions can be correctly
serialized and deserialized.
"""
import io
from types import FunctionType
from typing import List, Tuple

import pytest
from myserializer.serializer import Serializer

from serialization_inputs import test_basic, test_funcs_with_args
from serialization_options import serializers


def dumps_loads(item, serializer: Serializer):
    """dumps_loads function.

    Calls serializer.dumps(item), saves the result
    and returns serializer.loads(result).
    """
    serialized = serializer.dumps(item)
    deserialized = serializer.loads(serialized)
    return deserialized


def dump_load(item, serializer: Serializer):
    """dump_load function.

    Serializes item by calling serializer.dump
    and returns result of serializer.load.
    """
    with io.StringIO() as serialization_stream:
        serializer.dump(item, serialization_stream)
        serialization_stream.flush()
        serialization_stream.seek(0)
        deserialized = serializer.load(serialization_stream)
    return deserialized


@pytest.mark.parametrize('test_input', test_basic)
@pytest.mark.parametrize('serializer', serializers)
@pytest.mark.parametrize('cycle_serialization', [dumps_loads, dump_load])
def test_basic_serialization(test_input, serializer: Serializer,
                             cycle_serialization: FunctionType):
    """test_basic_serialization function.

    Checks that an object after cycle_serialization does not change:
    - type;
    - value.

    Preservation of value is checked by performing a comparison (==)
    of unserialized value and test_input.

    Args:
        test_input (Any): Object to be tested (serialized and deserialized).
        serializer (Serializer): The serializer to be used.

        cycle_serialization (FunctionType): A function that has two arguments:
        (object to be serialized, serializer to be used).
        It is expected to serialize and deserialize the object using
        the same Serializer object.
    """
    test_output = cycle_serialization(test_input, serializer)
    assert type(test_output) == type(test_input)
    assert test_output == test_input


@pytest.mark.parametrize('test_input', [
    '"just a string"', '[ "array", 1, 2 ]', '{"f" : "f"}', '{"a":"b"."c"}'
    '{ "unterminated ', '[rand ', '{"test"."d"}', '["a"."b","c"]',
    '{ "type" : "unknown" }', '{"\\u0'
])
@pytest.mark.parametrize('serializer', serializers)
def test_not_unpackable(test_input, serializer: Serializer):
    """test_not_unpackable function.

    Checks that the serializer raises Exception if input cannot be unpacked.
    """
    with pytest.raises(Exception):
        serializer.loads(test_input)


@pytest.mark.parametrize('test_func,test_args', test_funcs_with_args)
@pytest.mark.parametrize('serializer', serializers)
@pytest.mark.parametrize('cycle_serialization', [dumps_loads, dump_load])
def test_function_serialization(test_func: FunctionType,
                                test_args: List[Tuple],
                                serializer: Serializer,
                                cycle_serialization: FunctionType):
    """test_function_serialization function.

    Checks that the test_func after cycle_serialization does not change:
    - __doc__ value;
    - behaviour.

    Preservation of behaviour is checked by performing a comparison (==)
    of the results of calling unserialized function and initial function
    with provided arguments.

    Args:
        test_func (FunctionType): Function to be tested
        (serialized and deserialized).

        test_args (List): List of tuples of arguments to test on.

        serializer (Serializer): The serializer to be used.

        cycle_serialization (FunctionType): A function that has two arguments:
        (object to be serialized, serializer to be used).
        It is expected to serialize and deserialize the object using
        the same Serializer object.
    """
    serializer.globals = test_func.__globals__
    acquired_func = cycle_serialization(test_func, serializer)
    serializer.globals = None
    assert acquired_func.__doc__ == test_func.__doc__
    for test_arg in test_args:
        assert acquired_func(*test_arg) == test_func(*test_arg)
