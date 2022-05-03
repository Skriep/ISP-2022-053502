
_test_strings: list = [
    'abcdefg', 'with new\r\nlines', '\b\f\n\r\t \v\a',
    'unicode \u0014\u0ca7\u1337', '"\'!@@^*&^!@($!*@$)!@\'"'
]

_test_dicts: list = [
    {'test123': '123'}, {'12345': '27', '123': '45', '12': ['1', '2']},
    {'taet': ['123', '234', {'12\n': '123', '3': '4'}], 'f': '3'},
]

test_inputs: list = _test_strings + _test_dicts
