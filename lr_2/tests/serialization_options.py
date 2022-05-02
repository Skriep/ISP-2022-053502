import myserializer


serializers = list(map(myserializer.create_serializer, [
    'yaml'
]))
