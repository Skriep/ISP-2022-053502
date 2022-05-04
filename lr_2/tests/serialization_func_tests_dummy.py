"""Dummy module providing test function."""
import math

d = 4


def _t(arg):
    c = 2

    def _f():
        a = 123
        return math.sin(arg * a * c * d)

    return _f()
