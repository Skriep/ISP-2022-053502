import inspect
from pydoc import locate
from typing import Callable, Dict, List, cast
import re


class Packer:
    @staticmethod
    def pack(obj) -> 'Dict[str, str | List[Dict]]':
        data: 'Dict[str, str | List[Dict]]' = {}
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
        elif obj_type in (tuple, list, set):
            data['type'] = obj_type_str
            data['value'] = list(map(Packer.pack, obj))
        elif inspect.isroutine(obj):
            # TODO
            pass
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be packed')
        return data

    @staticmethod
    def unpack(data: 'Dict[str, str | List[Dict]]'):
        obj_type = str(data['type'])
        if obj_type == 'None':
            return None
        elif obj_type == 'bool':
            return True if data['value'] == 'True' else False
        elif obj_type in ('str', 'int', 'float', 'complex', 'bool'):
            callable = cast(Callable, locate(obj_type))
            return callable(data['value'])
        elif obj_type in ('tuple', 'list', 'dict', 'set'):
            callable = cast(Callable, locate(obj_type))
            return callable(map(Packer.unpack,
                                cast(List[Dict], data['value'])))
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be unpacked')
