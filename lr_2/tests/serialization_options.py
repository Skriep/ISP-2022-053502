import myserializer

implemented_types = [
    'yaml', 'toml', 'json'
]

serializers = list(map(myserializer.create_serializer,
                       implemented_types))

not_implemented_types = [
    'xml'
]
