import inspect
from pydoc import locate
from typing import Dict, List
import re


class Packer:
    @staticmethod
    def pack(obj) -> 'Dict[str, str | List[str]]':
        data = {}
        obj_type = type(obj)
        obj_type_str = re.findall("'(.+?)'", str(obj_type))[0]
        if obj is None:
            data['type'] = 'None'
        elif obj_type in (str, int, float, complex):
            data['type'] = obj_type_str
            data['value'] = str(obj)
        elif obj_type == dict:
            data['type'] = 'dict'
            data['value'] = list(map(Packer.pack, obj.items()))
        elif obj_type in (tuple, list):
            data['type'] = 'tuple'
            data['value'] = list(map(Packer.pack, obj))
        elif inspect.isroutine(obj):
            # TODO
            pass
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be packed')
        return data

    @staticmethod
    def unpack(data: 'Dict[str, str | List[str]]'):
        obj_type = data['type']
        if obj_type == 'None':
            return None
        elif obj_type in ('str', 'int', 'float', 'complex'):
            return locate(obj_type)(data['value'])
        elif obj_type in ('tuple', 'list', 'dict'):
            return locate(obj_type)(map(Packer.unpack, data['value']))
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be unpacked')
