import serialization


def main():
    json = serialization.create_serializer("json")
    yaml = serialization.create_serializer("yaml")
    toml = serialization.create_serializer("toml")


if __name__ == '__main__':
    main()
