import io
from contextlib import redirect_stdout

from psf2flf.utils import print_dict


def test_print_dict_simple():
    """Test with a simple, flat dictionary."""
    data = {"key1": "value1", "key2": 123}
    f = io.StringIO()
    with redirect_stdout(f):
        print_dict(data)
    output = f.getvalue()
    assert "key1: value1\n" in output
    assert "key2: 123\n" in output


def test_print_dict_nested():
    """Test with a nested dictionary."""
    data = {
        "level1_key1": "value1",
        "level1_key2": {
            "level2_key1": "value2",
            "level2_key2": {"level3_key1": "value3"},
        },
    }
    f = io.StringIO()
    with redirect_stdout(f):
        print_dict(data)
    output = f.getvalue()
    assert "level1_key1: value1\n" in output
    assert "level1_key2.level2_key1: value2\n" in output
    assert "level1_key2.level2_key2.level3_key1: value3\n" in output


def test_print_dict_empty():
    """Test with an empty dictionary."""
    data = {}
    f = io.StringIO()
    with redirect_stdout(f):
        print_dict(data)
    output = f.getvalue()
    assert output == ""


def test_print_dict_mixed_types():
    """Test with a dictionary containing various value types."""
    data = {"string": "hello", "integer": 42, "boolean": True, "none": None}
    f = io.StringIO()
    with redirect_stdout(f):
        print_dict(data)
    output = f.getvalue()
    assert "string: hello\n" in output
    assert "integer: 42\n" in output
    assert "boolean: True\n" in output
    assert "none: None\n" in output
