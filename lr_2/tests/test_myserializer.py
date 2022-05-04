from myserializer import create_serializer
from myserializer.serializer import Serializer
from serialization_options import implemented_types as implemented
from serialization_options import not_implemented_types as not_implemented
import pytest
from typing import List
import random


def randomize_uppercase(lst: List[str]):
    result = []
    random.seed(0)
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
    assert isinstance(create_serializer(serializer_type), Serializer)


@pytest.mark.parametrize(
    'serializer_type', not_implemented + randomize_uppercase(not_implemented))
def test_not_implemented(serializer_type):
    with pytest.raises(NotImplementedError):
        create_serializer(serializer_type)
