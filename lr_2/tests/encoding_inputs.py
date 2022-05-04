"""Encoding Inputs.

This module provides a number of test inputs to be used by PyTest.
It primarily targets testing encoders and decoders that are compatible
with myserializer.packer.Packer.

Attributes:
    test_inputs (list): A list of test inputs, including:
    - test strings
    - test dicts
    - test lists
"""

_test_strings: list = [
    'abcdefg', 'with new\r\nlines', '\b\f\n\r\t \v\a', '',
    'unicode \u0014\u0ca7\u1337', '"\'!@@^*&^!@($!*@$)!@\'"'
]

_test_dicts: list = [
    {'test123': '123'}, {'12345': '27', '123': '45', '12': ['1', '2']},
    {'taet': ['123', '234', {'12\n': '123', '3': '4'}], 'f': '3'}, {}
]

_test_lists: list = [
    ['1'], ['1', '2', '3'], ['\x12', '2', ['1', '', {}], {'1': ['2', '']}]
]

test_inputs: list = _test_strings + _test_dicts + _test_lists
