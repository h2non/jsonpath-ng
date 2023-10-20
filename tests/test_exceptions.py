import pytest

from jsonpath_ng import parse as base_parse
from jsonpath_ng.exceptions import JsonPathParserError
from jsonpath_ng.ext import parse as ext_parse


@pytest.mark.parametrize(
    "path",
    (
        "foo[*.bar.baz",
        "foo.bar.`grandparent`.baz",
        "foo[*",
        # `len` extension not available in the base parser
        "foo.bar.`len`",
    ),
)
def test_rw_exception_subclass(path):
    with pytest.raises(JsonPathParserError):
        base_parse(path)


@pytest.mark.parametrize(
    "path",
    (
        "foo[*.bar.baz",
        "foo.bar.`grandparent`.baz",
        "foo[*",
    ),
)
def test_ext_exception_subclass(path):
    with pytest.raises(JsonPathParserError):
        ext_parse(path)
