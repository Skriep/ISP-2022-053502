_int_tests: list = [
    1, 2, 12, 13434, -134134, 0, 7
]

_bool_tests: list = [
    True, False, (False, True), [True, (1, 2, 'k9')]
]

_dict_tests: list = [
    {1: 2}, {'a': 'b'}, {None: 'ok'},
    {'key': 'value', 123: 456, 12.3: 4.56, (1.4j + 3): "that's complex!",
     (1, 2, 3): (4, 5, 6)},
    {'deep': {'deep': {'deep': {'deep': {'deep': {'deep': {'deep': 1}}}}}}}
]

_set_tests: list = [
    {1, 2, 3, 'this is SET', True, 13.4},
    frozenset({1, 2, '3', False, 3.14})
]

_range_tests: list = [
    range(100), range(0, 1, 2), range(25, -10, -1)
]

_bytes_tests: list = [
    b'\x00\x01\x02 abc 123 \n\r -- \x93', b'123', b'bytes',
    bytearray(b'123'), bytearray((1, 2, 5, 3, 2, 6, 235, 12, 123))
]

test_inputs: list = _int_tests + _bool_tests + _dict_tests + \
    _set_tests + _range_tests + _bytes_tests
