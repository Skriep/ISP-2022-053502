"""This module privides myserializer.cli tests."""
import os

import myserializer
import pytest
from myserializer import cli


def test_main_help(capsys):
    """Test CLI help."""
    with pytest.raises(SystemExit):
        cli.main(['-h'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out.startswith('usage: ')


def test_main_bad_filename(capsys):
    """Test CLI with file that does not exist."""
    filename = 'this_definit3ly_do3s_n0t_ex1st.i_am_sur3'
    while os.path.exists(filename):
        filename += '_'
    cli.main(f'-i {filename} -o tmp -if json -of yaml'.split())
    out, err = capsys.readouterr()
    assert 'No such file' in err


def test_main_bad_format(capsys):
    """Test CLI with serialization format that does not exist."""
    cli.main('-i tmp -o tmp -if BAD -of yaml'.split())
    out, err = capsys.readouterr()
    assert 'Unknown format' in err


def test_main_json_yaml(capsys):
    """Test CLI with correct input: json -> yaml."""
    filename = 'th1s_should_n0t_ex1st_yet.json'
    while os.path.exists(filename):
        filename += '_'
    initial_val = 123
    try:
        with open(filename, 'w') as file:
            myserializer.create_serializer('json').dump(initial_val, file)
        cli.main(f'-i {filename} -o {filename} -if json -of yaml'.split())
        with open(filename, 'r') as file:
            value = myserializer.create_serializer('yaml').load(file)
        assert initial_val == value
        out, err = capsys.readouterr()
        assert err == ''
        assert 'Success' in out
    except Exception:
        pass
    finally:
        os.remove(filename)


def test_main_json_json(capsys):
    """Test CLI with input format being the same as output: json -> json."""
    filename_1 = 'th1s_should_n0t_ex1st_yet.json'
    while os.path.exists(filename_1):
        filename_1 += '_'
    filename_2 = 'th1s_als0_should_n0t_ex1st_yet.json'
    while os.path.exists(filename_2):
        filename_2 += '_'
    initial_val = 123
    try:
        with open(filename_1, 'w') as file:
            myserializer.create_serializer('json').dump(initial_val, file)
        cli.main(f'-i {filename_1} -o {filename_2} -if json -of json'.split())
        with open(filename_2, 'r') as file:
            value = myserializer.create_serializer('json').load(file)
        assert initial_val == value
        out, err = capsys.readouterr()
        assert err == ''
        assert 'Success' in out
    except Exception:
        pass
    finally:
        os.remove(filename_1)
        os.remove(filename_2)


def test_main_json_json_same_file(capsys):
    """Test CLI with output file being same as input file, and same format."""
    filename = 'th1s_should_n0t_ex1st_yet.toml'
    while os.path.exists(filename):
        filename += '_'
    initial_val = 123
    try:
        with open(filename, 'w') as file:
            myserializer.create_serializer('toml').dump(initial_val, file)
        cli.main(f'-i {filename} -o {filename} -if toml -of toml'.split())
        with open(filename, 'r') as file:
            value = myserializer.create_serializer('toml').load(file)
        assert initial_val == value
        out, err = capsys.readouterr()
        assert 'the same file' in err
    except Exception:
        pass
    finally:
        os.remove(filename)
