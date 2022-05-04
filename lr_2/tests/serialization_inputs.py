"""Serialization Inputs.

This module provides a number of test inputs to be used by PyTest.
It primarily targets testing serializers implemented by myserializer module.

Attributes:
    test_basic (list): A list of test inputs, including
    basic types such as int, float, complex, bool, dict, list, set, frozenset,
    tuple, range, bytes, bytearray, str.

    test_funcs_with_args (list): A list of tuples, where the first element is
    a function, and the second one is a list of test argument tuples.
"""
from types import FunctionType
from typing import List, Tuple


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

test_basic: list = _int_tests + _bool_tests + _dict_tests + \
    _set_tests + _range_tests + _bytes_tests


def _get_test_funcs() -> list:
    def _get_func_1():
        import math
        c = 42

        def f(x):
            a = 123
            return math.sin(x * a * c)
        return f

    def _get_func_2():
        import math
        d = 4

        def _t(arg):
            c = 2

            def _f():
                a = 123
                return math.sin(arg * a * c * d)
            return _f()
        return _t

    def _get_func_3():
        import math
        b = 4

        def _t(arg, default=3):
            """Test docstring."""
            a = 225
            return math.sin(arg * a * b + default)
        return _t

    def _get_func_4():
        import math
        b = 7

        def _a(arg, default=7):
            a = 27
            return math.sin(arg * a * b + default)

        def _b(arg, default=3):
            """Docstring."""
            a = 225
            if arg > 0:
                return _a(arg * a * b + default)
            else:
                return _a(a * b, default - arg)
        return _b

    import math

    def _test_func_5(a, b, c):
        def abs(x):
            return x if x >= 0 else -x
        return math.ceil(a * math.sqrt(abs(b)) + c)

    return [
        (_get_func_1(), [(x,) for x in [1, 3, -7, 777.35]]),
        (_get_func_2(), [(x,) for x in [10, -45, 39, 13]]),
        (_get_func_3(), [(1,), (7,), (-64, 4), (10, 5), (25,)]),
        (_get_func_4(), [(12,), (4,), (-4, 5), (1, 56), (12,)]),
        (_test_func_5, [(1, 3, 5), (-1, -3, 4), (4.2, 23.4, 2345.3)])
    ]


test_funcs_with_args: List[Tuple[FunctionType,
                                 List[Tuple]]] = _get_test_funcs()
