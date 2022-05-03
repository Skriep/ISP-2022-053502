from typing import Dict, List, cast


STR_ESCAPED_CHARS = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\x7f': '\\u007f'
}

for i in range(0x20):
    STR_ESCAPED_CHARS.setdefault(chr(i), f'\\u{i:04x}')


def str_json_escape(s: str) -> str:
    for k, v in STR_ESCAPED_CHARS.items():
        s = s.replace(k, v)
    return s


class JsonEncoder:
    item_separator = ','
    key_separator = ':'

    def __init__(self, separators=None):
        if separators is not None:
            self.item_separator, self.key_separator = separators

    def encode(self, obj: 'str | Dict[str, str | List[Dict]] | List[Dict]'
               ) -> str:
        obj_type = type(obj)
        if obj_type == str:
            return self._encode_str(cast(str, obj))
        elif obj_type == dict:
            return self._encode_dict(cast(dict, obj))
        elif obj_type == list:
            return self._encode_list(cast(list, obj))
        else:
            raise NotImplementedError(f'The object of type "{obj_type}" '
                                      'cannot be JSON encoded')

    def _encode_str(self, obj: str):
        return f'"{str_json_escape(obj)}"'

    def _encode_list(self, obj: List[Dict]) -> str:
        buf = '['
        first_val = True
        for val in obj:
            if not first_val:
                buf += self.item_separator
            else:
                first_val = False
            buf += self.encode(val)
        return buf + ']'

    def _encode_dict(self, obj: Dict[str, 'str | List[Dict]']) -> str:
        buf = '{'
        first_pair = True
        for k, v in obj.items():
            if not first_pair:
                buf += self.item_separator
            else:
                first_pair = False
            buf += self.encode(k)
            buf += self.key_separator
            buf += self.encode(v)
        return buf + '}'
