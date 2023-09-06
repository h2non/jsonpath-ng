import pytest

from jsonpath_ng import parse as rw_parse
from jsonpath_ng.exceptions import JSONPathError, JsonPathParserError
from jsonpath_ng.ext import parse as ext_parse


def test_rw_exception_class():
    with pytest.raises(JSONPathError):
        rw_parse('foo.bar.`grandparent`.baz')


def test_rw_exception_subclass():
    with pytest.raises(JsonPathParserError):
        rw_parse('foo.bar.`grandparent`.baz')


def test_ext_exception_subclass():
    with pytest.raises(JsonPathParserError):
        ext_parse('foo.bar.`grandparent`.baz')
