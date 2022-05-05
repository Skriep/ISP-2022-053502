"""JsonDecoder module.

This module can decode objects from JSON strings.

If imported as module, the class JsonDecoder is available.
"""
from io import StringIO
from typing import Dict, List, TextIO, Tuple, cast

WHITESPACE_CHARS = ' \n\r'

STR_ESCAPED = {
    '\\': '\\',
    '"': '"',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    '/': '/'
}

for i in range(0x20):
    STR_ESCAPED.setdefault(f'\\u{i:04x}', chr(i))


def _str_json_unescape(s: str) -> str:
    for k, v in STR_ESCAPED.items():
        s = s.replace(k, v)
    return s


def _read_chars(stream: TextIO, amount: int) -> str:
    chars = stream.read(amount)
    if len(chars) != amount:
        raise ValueError('Unexpected end of stream')
    return chars


class JsonDecoder:
    """The class provides methods for object decoding from JSON format.

    Provided functions:
    - decode - decode object from JSON string.

    Suppurted object types:
    - str;
    - dict;
    - list.
    """

    item_separator = ','
    key_separator = ':'

    def __init__(self, separators: 'Tuple[str, str] | None' = None):
        r"""__init__ method.

        Args:
            separators (tuple, optional) - a tuple of (item_sep, key_sep).
            If not specified, the default values are used:
            - item_sep = ',';
            - key_sep = ':'.

        Note:
            If defined, each of the separators may only contain one character,
            or one character and many whitespaces. In the latter case all
            whitespaces are ignored.
            Whitespaces are ' ', '\n', '\r'.
        """
        if separators is not None:
            item_separator, key_separator = separators
            item_separator = item_separator.strip(WHITESPACE_CHARS)
            key_separator = key_separator.strip(WHITESPACE_CHARS)
            if len(item_separator) != 1 or len(key_separator) != 1:
                raise ValueError('Separators must consist of '
                                 '1 non-whitespace char')
            self.item_separator = item_separator
            self.key_separator = key_separator

    def decode(self, s: 'str | TextIO') -> 'str | Dict | List':
        """Decode python object from JSON string or TextIO."""
        if type(s) is str:
            with StringIO(cast(str, s)) as _stream:
                return self.decode(_stream)
        stream = cast(TextIO, s)
        while True:
            ch = _read_chars(stream, 1)
            if ch in WHITESPACE_CHARS:
                continue
            return self._decode(stream, ch)

    def _decode(self, stream: TextIO, first_char: str):
        """Decode object from TextIO assuming previous char was first_char."""
        if first_char == '{':
            return self._decode_dict(stream)
        elif first_char == '[':
            return self._decode_list(stream)
        elif first_char == '"':
            return self._decode_str(stream)
        else:
            raise ValueError(f'Unexpected character "{first_char}"')

    def _decode_str(self, stream: TextIO) -> str:
        buf = ['']
        while (ch := _read_chars(stream, 1)) != '"':
            if ch == '\\':
                next_ch = _read_chars(stream, 1)
                if next_ch == 'u':
                    unicode_hex = _read_chars(stream, 4)
                    unicode_val = int(unicode_hex, 16)
                    buf.append(chr(unicode_val))
                else:
                    buf.append(_str_json_unescape(next_ch))
            else:
                buf.append(ch)
        return ''.join(buf)

    def _decode_list(self, stream: TextIO) -> List:
        result: list = []
        first_val = True
        while (ch := _read_chars(stream, 1)) != ']':
            if ch in WHITESPACE_CHARS:
                continue
            if not first_val:
                if ch != self.item_separator:
                    raise ValueError(
                        f'Unexpected character "{ch}". '
                        f'Expected item separator: "{self.item_separator}"')
                value = self.decode(stream)
            else:
                value = self._decode(stream, ch)
                first_val = False
            result.append(value)
        return result

    def _decode_dict(self, stream: TextIO) -> Dict:
        result: dict = {}
        first_pair = True
        while (ch := _read_chars(stream, 1)) != '}':
            if ch in WHITESPACE_CHARS:
                continue
            if not first_pair:
                if ch != self.item_separator:
                    raise ValueError(
                        f'Unexpected character "{ch}". '
                        f'Expected item separator: "{self.item_separator}"')
                key = self.decode(stream)
            else:
                key = self._decode(stream, ch)
                first_pair = False
            next_char = _read_chars(stream, 1)
            while next_char in WHITESPACE_CHARS:
                next_char = _read_chars(stream, 1)
            if next_char != self.key_separator:
                raise ValueError(
                    f'Unexpected character "{next_char}". '
                    f'Expected key separator: "{self.key_separator}"')
            value = self.decode(stream)
            result.setdefault(key, value)
        return result
