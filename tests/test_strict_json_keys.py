import pytest
from examples.strict_json_decoder import strict_loads, DuplicateKeyError


def test_duplicate_root_key():
    with pytest.raises(DuplicateKeyError):
        strict_loads('{"x":1,"x":2}')


def test_duplicate_nested_key():
    with pytest.raises(DuplicateKeyError):
        strict_loads('{"nested":{"x":1,"x":2}}')


def test_distinct_nested_keys():
    assert strict_loads('{"a":{"x":1},"b":{"x":2}}')["b"]["x"] == 2
