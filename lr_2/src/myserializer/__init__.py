"""MySerializer module.

This module can serialize and deserialize objects to (from)
string or TextIO in different serialization formats.

If imported as module, the method create_serializer is available.
"""
from myserializer.my_json import JsonSerializer
from myserializer.my_yaml import YamlSerializer
from myserializer.my_toml import TomlSerializer
from myserializer.serializer import Serializer


def create_serializer(serializer_type: str) -> Serializer:
    """Create serializer of specific type.

    Supported serializer types:
    - json;
    - yaml;
    - toml.

    Args:
        serializer_type (str): serializer type, case-insensitive.

    Returns:
        instance of class Serializer.
    """
    serializer_type = serializer_type.lower()
    if serializer_type == 'json':
        return JsonSerializer()
    elif serializer_type == 'yaml':
        return YamlSerializer()
    elif serializer_type == 'toml':
        return TomlSerializer()
    else:
        raise NotImplementedError('Unknown serializer type')
