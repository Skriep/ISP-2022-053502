from myserializer.my_json import JsonSerializer
from myserializer.my_yaml import YamlSerializer
from myserializer.my_toml import TomlSerializer
from myserializer.serializer import Serializer


def create_serializer(serializer_type: str) -> Serializer:
    serializer_type = serializer_type.lower()
    if serializer_type == 'json':
        return JsonSerializer()
    elif serializer_type == 'yaml':
        return YamlSerializer()
    elif serializer_type == 'toml':
        return TomlSerializer()
    else:
        raise NotImplementedError('Unknown serializer type')
