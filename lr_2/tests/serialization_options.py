"""Serialization Options.

This module provides lists of serialization formats and serializers.

Attributes:
    implemented_formats (list): A list of strings, representing formats
    that are expected to be implemented by myserializer.

    serializers (list): A list of pre-created serializers for those formats
    listed in implemented_formats. Serializers are created by calling
    myserializer.create_serializer(format).

    not_implemented_formats (list):A list of strings, representing formats
    that are not expected to be implemented by myserializer.
"""
import myserializer

implemented_formats = [
    'yaml', 'toml', 'json'
]

serializers = list(map(myserializer.create_serializer,
                       implemented_formats))

not_implemented_formats = [
    'xml', 'bson'
]
