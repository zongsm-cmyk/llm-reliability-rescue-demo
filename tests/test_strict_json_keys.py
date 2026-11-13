import pytest
from examples.strict_json_decoder import strict_loads, DuplicateKeyError, NonFiniteNumberError


def test_duplicate_root_key():
    with pytest.raises(DuplicateKeyError):
        strict_loads('{"x":1,"x":2}')


def test_duplicate_nested_key():
    with pytest.raises(DuplicateKeyError):
        strict_loads('{"nested":{"x":1,"x":2}}')


def test_distinct_nested_keys():
    assert strict_loads('{"a":{"x":1},"b":{"x":2}}')["b"]["x"] == 2


@pytest.mark.parametrize("token", ["1e999", "-1e999"])
@pytest.mark.parametrize("template", ["{}", '{{"value":{}}}', '{{"nested":[[{{"value":{}}}]]}}'])
def test_numeric_overflow_is_rejected(token, template):
    with pytest.raises(NonFiniteNumberError, match="Non-finite JSON number"):
        strict_loads(template.format(token))


@pytest.mark.parametrize("token", ["1.25", "-1.25", "1e308", "-1e308", "0.0"])
def test_finite_numbers_remain_floats(token):
    value = strict_loads('{"nested":[' + token + ']}')["nested"][0]
    assert type(value) is float
    assert value == float(token)
