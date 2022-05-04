import inspect
import marshal
from pydoc import locate
from types import CellType, FunctionType
from typing import Any, Callable, Dict, List, cast
import re
import builtins


def _make_cell(contents):
    _contents = contents

    def internal():
        return _contents

    return internal.__closure__[0]


class Packer:
    @staticmethod
    def pack(obj) -> 'Dict[str, str | List[Dict] | Dict]':
        data: 'Dict[str, str | List[Dict] | Dict]' = {}
        obj_type = type(obj)
        obj_type_str = re.findall("'(.+?)'", str(obj_type))[0]
        if obj is None:
            data['type'] = 'None'
        elif obj_type in (str, int, float, complex, bool):
            data['type'] = obj_type_str
            data['value'] = str(obj)
        elif obj_type == dict:
            data['type'] = 'dict'
            data['value'] = list(map(Packer.pack, obj.items()))
        elif obj_type in (tuple, list, set, frozenset, bytes, bytearray):
            data['type'] = obj_type_str
            data['value'] = list(map(Packer.pack, obj))
        elif obj_type == range:
            data['type'] = 'range'
            obj = cast(range, obj)
            data['start'] = Packer.pack(obj.start)
            data['stop'] = Packer.pack(obj.stop)
            data['step'] = Packer.pack(obj.step)
        elif obj_type == CellType:
            data['type'] = 'cell'
            data['value'] = Packer.pack(cast(CellType, obj).cell_contents)
        elif inspect.isfunction(obj):
            data['type'] = 'function'
            data['doc'] = Packer.pack(obj.__doc__)
            data['name'] = Packer.pack(obj.__name__)
            data['code'] = Packer.pack(marshal.dumps(obj.__code__))
            data['defaults'] = Packer.pack(obj.__defaults__)
            data['closure'] = Packer.pack(obj.__closure__)
        else:
            print(obj)
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be packed')
        return data

    @staticmethod
    def unpack(data: 'Dict[str, str | List[Dict] | Dict]',
               globals: Dict[str, Any] = None):
        obj_type = str(data['type'])
        if obj_type == 'None':
            return None
        elif obj_type == 'bool':
            return True if data['value'] == 'True' else False
        elif obj_type in ('str', 'int', 'float', 'complex', 'bool'):
            callable = cast(Callable, locate(obj_type))
            return callable(data['value'])
        elif obj_type in ('tuple', 'list', 'dict', 'set', 'frozenset',
                          'bytes', 'bytearray'):
            callable = cast(Callable, locate(obj_type))
            return callable(map(Packer.unpack,
                                cast(List[Dict], data['value'])))
        elif obj_type == 'range':
            start = Packer.unpack(cast(Dict, data['start']))
            stop = Packer.unpack(cast(Dict, data['stop']))
            step = Packer.unpack(cast(Dict, data['step']))
            return range(start, stop, step)
        elif obj_type == 'cell':
            cell_contents = Packer.unpack(cast(Dict, data['value']))
            return _make_cell(cell_contents)
        elif obj_type == 'function':
            if globals is None:
                globals = builtins.globals()
            doc = Packer.unpack(cast(Dict, data['doc']))
            name = Packer.unpack(cast(Dict, data['name']))
            code_marshalled = Packer.unpack(cast(Dict, data['code']))
            code = marshal.loads(code_marshalled)
            defaults = Packer.unpack(cast(Dict, data['defaults']))
            closure = Packer.unpack(cast(Dict, data['closure']))
            func = FunctionType(code, globals, name, defaults, closure)
            func.__doc__ = doc
            return func
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be unpacked')
