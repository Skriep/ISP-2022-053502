"""Command line interface for myserializer."""
import argparse
import sys
import myserializer
from myserializer.serializer import Serializer
import shutil


def _print_err(error):
    print(f'Error: {error}', file=sys.stderr)


def _try_get_serializer(serializer_format: str) -> 'Serializer | None':
    try:
        return myserializer.create_serializer(serializer_format)
    except NotImplementedError:
        _print_err(f'Unknown format "{serializer_format}"')
    return None


def main(argv=None):
    """Run convertation of file formats."""
    parser = argparse.ArgumentParser(
        description='Change serialized file format.')
    parser.add_argument('-i', '--input_file', help='input filename',
                        required=True)
    parser.add_argument('-o', '--output_file', help='output filename',
                        required=True)
    parser.add_argument('-if', '--input_format', help='input format',
                        required=True)
    parser.add_argument('-of', '--output_format', help='output format',
                        required=True)

    args = parser.parse_args(argv)

    input_filename = args.input_file
    output_filename = args.output_file
    input_format = args.input_format
    output_format = args.output_format

    if input_format == output_format:
        try:
            shutil.copy(input_filename, output_filename)
            print('Success!')
        except Exception as e:
            _print_err(e)
        finally:
            return

    if ((input_serializer := _try_get_serializer(input_format)) is None or
            (output_serializer := _try_get_serializer(output_format)) is None):
        return

    try:
        with open(input_filename, 'r') as input_file:
            loaded = input_serializer.load(input_file)
        with open(output_filename, 'w') as output_file:
            output_serializer.dump(loaded, output_file)
        print('Success!')
    except Exception as e:
        _print_err(e)
        return


if __name__ == '__main__':
    main()
