import copy
from contextlib import nullcontext as does_not_raise

import pytest

from jsonpath_ng.ext import parse


@pytest.mark.parametrize(
    "string, initial_data, expected_result",
    (
        ("$.foo", {}, {"foo": 42}),
        ("$.foo.bar", {}, {"foo": {"bar": 42}}),
        ("$.foo.bar", {"foo": None}, {"foo": {"bar": 42}}),
        ("$.foo[0]", {}, {"foo": [42]}),
        ("$.foo[0]", {"foo": None}, {"foo": [42]}),
        ("$.foo[1]", {}, {"foo": [{}, 42]}),
        ("$.foo[0].bar", {}, {"foo": [{"bar": 42}]}),
        ("$.foo[1].bar", {}, {"foo": [{}, {"bar": 42}]}),
        ("$.foo[0][0]", {}, {"foo": [[42]]}),
        ("$.foo[1][1]", {}, {"foo": [{}, [{}, 42]]}),
        ("foo[0]", {}, {"foo": [42]}),
        ("foo[1]", {}, {"foo": [{}, 42]}),
        ("foo", {}, {"foo": 42}),
        #
        # Initial data can be a list if we expect a list back.
        ("[0]", [], [42]),
        ("[1]", [], [{}, 42]),
        #
        # Convert initial data to a list, if necessary.
        ("[0]", {}, [42]),
        ("[1]", {}, [{}, 42]),
        #
        (
            'foo[?bar="baz"].qux',
            {
                "foo": [
                    {"bar": "baz"},
                    {"bar": "bizzle"},
                ]
            },
            {"foo": [{"bar": "baz", "qux": 42}, {"bar": "bizzle"}]},
        ),
        ("[1].foo", [{"foo": 1}, {"bar": 2}], [{"foo": 1}, {"foo": 42, "bar": 2}]),
    ),
)
def test_update_or_create(string, initial_data, expected_result):
    jsonpath = parse(string)
    result = jsonpath.update_or_create(initial_data, 42)
    assert result == expected_result


def test_find_or_create_replaces_null_intermediate_fields():
    data = {"folder": {"document": None}}
    jsonpath = parse("$.folder.document.doc_a.value")

    matches = jsonpath.find_or_create(data)

    assert [match.value for match in matches] == [{}]
    assert data == {"folder": {"document": {"doc_a": {"value": {}}}}}


@pytest.mark.parametrize("value", (False, 0, "", []))
def test_update_or_create_does_not_replace_non_null_intermediates(value):
    data = {"foo": value}

    with pytest.raises(TypeError):
        parse("$.foo.bar").update_or_create(data, 42)

    assert data == {"foo": value}


@pytest.mark.parametrize(
    "string, initial_data, expectation",
    (
        # Slice not supported
        ("foo[0:1]", {}, does_not_raise()),
        #
        # Filter does not create items to meet criteria
        ('foo[?bar="baz"].qux', {}, does_not_raise()),
        #
        # Does not convert initial data to a dictionary
        ("foo", [], pytest.raises(TypeError)),
    ),
)
def test_unsupported_classes(string, initial_data, expectation):
    copied_initial_data = copy.copy(initial_data)
    jsonpath = parse(string)
    with expectation:
        result = jsonpath.update_or_create(initial_data, 42)
        assert result != copied_initial_data
