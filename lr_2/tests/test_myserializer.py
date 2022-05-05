"""myserializer tests.

This module provides a number of tests to be used by PyTest.
It targets testing myserializer module:
- Checking if create_serializer returns an instance of Serializer
for valid inputs;
- Checking if create_serializer raises NotImplementedError for those
formats that are not expected to be implemented.
"""
import random
from typing import List

import pytest
from myserializer import create_serializer
from myserializer.serializer import Serializer

from serialization_options import implemented_formats as implemented
from serialization_options import not_implemented_formats as not_implemented


def randomize_uppercase(lst: List[str], seed: int = 0):
    """randomize_uppercase function.

    Randomly converts one character in each string from lst to uppercase.

    Args:
        lst (list): The list of strings.
        seed (int): The seed to be used to initialize random.

    Returns:
        list: A list of modified strings from lst.
    """
    result = []
    random.seed(seed)
    for item in lst:
        pos = random.randint(0, len(item) - 1)
        modified = ''
        if pos != 0:
            modified += item[:pos]
        modified += item[pos].upper()
        if pos < len(item):
            modified += item[pos+1:]
        result.append(modified)
    return result


@pytest.mark.parametrize('serializer_type',
                         implemented + randomize_uppercase(implemented))
def test_implemented(serializer_type):
    """test_implemented function.

    Tests myserializer.create_serializer function by calling it
    with provided serializer_type checking if returned value is instance of
    myserializer.serializer.Serializer.

    It is expected for serializer_type format to be implemented.
    """
    assert isinstance(create_serializer(serializer_type), Serializer)


@pytest.mark.parametrize(
    'serializer_type', not_implemented + randomize_uppercase(not_implemented))
def test_not_implemented(serializer_type):
    """test_not_implemented function.

    Tests myserializer.create_serializer function by calling it
    with provided serializer_type checking if returned value is instance of
    myserializer.serializer.Serializer.

    serializer_type is expected to not be implemented by myserializer.
    It is expected for myserializer.create_serializer to raise
    NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        create_serializer(serializer_type)
