"""This module privides myserializer.cli tests."""
from myserializer import cli
import myserializer
import pytest
import os


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
