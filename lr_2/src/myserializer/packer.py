import inspect
import marshal
from pydoc import locate
from types import CellType, FunctionType
from typing import Any, Callable, Dict, List, cast
import re
import builtins
from base64 import b64encode, b64decode


def _make_cell(contents):
    _contents = contents

    def internal():
        return _contents

    return internal.__closure__[0]


class Packer:
    def __init__(self, globals: Dict[str, Any] = None) -> None:
        self.globals = globals

    def pack(self, obj) -> 'Dict[str, str | List[Dict] | Dict]':
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
            data['value'] = list(map(self.pack, obj.items()))
        elif obj_type in (tuple, list, set, frozenset):
            data['type'] = obj_type_str
            data['value'] = list(map(self.pack, obj))
        elif obj_type in (bytes, bytearray):
            data['type'] = obj_type_str
            data['value'] = self.pack(b64encode(obj).decode())
        elif obj_type == range:
            data['type'] = 'range'
            obj = cast(range, obj)
            data['start'] = self.pack(obj.start)
            data['stop'] = self.pack(obj.stop)
            data['step'] = self.pack(obj.step)
        elif obj_type == CellType:
            data['type'] = 'cell'
            data['value'] = self.pack(cast(CellType, obj).cell_contents)
        elif inspect.ismodule(obj):
            data['type'] = 'module'
            data['name'] = self.pack(obj.__name__)
        elif inspect.isfunction(obj):
            data['type'] = 'function'
            data['doc'] = self.pack(obj.__doc__)
            data['name'] = self.pack(obj.__name__)
            data['code'] = self.pack(marshal.dumps(obj.__code__))
            data['defaults'] = self.pack(obj.__defaults__)
            data['closure'] = self.pack(obj.__closure__)
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be packed')
        return data

    def unpack(self, data: 'Dict[str, str | List[Dict] | Dict]') -> Any:
        obj_type = str(data['type'])
        if obj_type == 'None':
            return None
        elif obj_type == 'bool':
            return True if data['value'] == 'True' else False
        elif obj_type in ('str', 'int', 'float', 'complex', 'bool'):
            callable = cast(Callable, locate(obj_type))
            return callable(data['value'])
        elif obj_type in ('tuple', 'list', 'dict', 'set', 'frozenset'):
            callable = cast(Callable, locate(obj_type))
            return callable(map(self.unpack,
                                cast(List[Dict], data['value'])))
        elif obj_type in ('bytes', 'bytearray'):
            result = b64decode(self.unpack(cast(Dict, data['value'])))
            if obj_type == 'bytearray':
                return bytearray(result)
            return result
        elif obj_type == 'range':
            start = self.unpack(cast(Dict, data['start']))
            stop = self.unpack(cast(Dict, data['stop']))
            step = self.unpack(cast(Dict, data['step']))
            return range(start, stop, step)
        elif obj_type == 'cell':
            cell_contents = self.unpack(cast(Dict, data['value']))
            return _make_cell(cell_contents)
        elif obj_type == 'module':
            name = self.unpack(cast(Dict, data['name']))
            name = cast(str, name)
            if self.globals and name in self.globals:
                return self.globals[name]
            else:
                return __import__(name, self.globals)
        elif obj_type == 'function':
            globals = self.globals
            if globals is None:
                globals = builtins.globals()
            doc = self.unpack(cast(Dict, data['doc']))
            name = self.unpack(cast(Dict, data['name']))
            code_marshalled = self.unpack(cast(Dict, data['code']))
            code = marshal.loads(code_marshalled)
            defaults = self.unpack(cast(Dict, data['defaults']))
            closure = self.unpack(cast(Dict, data['closure']))
            func = FunctionType(code, globals, name, defaults, closure)
            func.__doc__ = doc
            return func
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be unpacked')
