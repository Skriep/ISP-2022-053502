from serialization import my_toml
from serialization import my_yaml
from serialization import my_json


def create_serializer(serializer_type: str):
    serializer_type = serializer_type.lower()
    if serializer_type == 'json':
        return my_json
    elif serializer_type == 'yaml':
        return my_yaml
    elif serializer_type == 'toml':
        return my_toml
    else:
        raise NotImplementedError('Unknown serializer type')
