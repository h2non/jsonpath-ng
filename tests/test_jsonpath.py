import copy

import pytest
from typing import Callable
from jsonpath_ng.ext.parser import parse as ext_parse
from jsonpath_ng.jsonpath import DatumInContext, Fields, Root, This
from jsonpath_ng.lexer import JsonPathLexerError
from jsonpath_ng.parser import parse as base_parse
from jsonpath_ng import JSONPath

from .helpers import assert_full_path_equality, assert_value_equality


@pytest.mark.parametrize(
    "path_arg, context_arg, expected_path, expected_full_path",
    (
        (None, None, This(), This()),
        (Root(), None, Root(), Root()),
        (Fields("foo"), "unimportant", Fields("foo"), Fields("foo")),
        (
            Fields("foo"),
            DatumInContext("unimportant", path=Fields("baz"), context="unimportant"),
            Fields("foo"),
            Fields("baz").child(Fields("foo")),
        ),
    ),
)
def test_datumincontext_init(path_arg, context_arg, expected_path, expected_full_path):
    datum = DatumInContext(3, path=path_arg, context=context_arg)
    assert datum.path == expected_path
    assert datum.full_path == expected_full_path


def test_datumincontext_in_context():
    d1 = DatumInContext(3, path=Fields("foo"), context=DatumInContext("bar"))
    d2 = DatumInContext(3).in_context(path=Fields("foo"), context=DatumInContext("bar"))
    assert d1 == d2


def test_datumincontext_in_context_nested():
    sequential_calls = (
        DatumInContext(3)
        .in_context(path=Fields("foo"), context="whatever")
        .in_context(path=Fields("baz"), context="whatever")
    )
    nested_calls = DatumInContext(3).in_context(
        path=Fields("foo"),
        context=DatumInContext("whatever").in_context(
            path=Fields("baz"), context="whatever"
        ),
    )
    assert sequential_calls == nested_calls


parsers = pytest.mark.parametrize(
    "parse",
    (
        pytest.param(base_parse, id="parse=jsonpath_ng.parser.parse"),
        pytest.param(ext_parse, id="parse=jsonpath_ng.ext.parser.parse"),
    ),
)


update_test_cases = (
    #
    # Fields
    # ------
    #
    ("foo", {"foo": 1}, 5, {"foo": 5}),
    ("$.*", {"foo": 1, "bar": 2}, 3, {"foo": 3, "bar": 3}),
    #
    # Indexes
    # -------
    #
    ("[0]", ["foo", "bar", "baz"], "test", ["test", "bar", "baz"]),
    ("[0, 1]", ["foo", "bar", "baz"], "test", ["test", "test", "baz"]),
    ("[0, 1]", ["foo", "bar", "baz"], ["test", "test 1"], ["test", "test 1", "baz"]),
    #
    # Slices
    # ------
    #
    ("[0:2]", ["foo", "bar", "baz"], "test", ["test", "test", "baz"]),
    #
    # Root
    # ----
    #
    ("$", "foo", "bar", "bar"),
    #
    # This
    # ----
    #
    ("`this`", "foo", "bar", "bar"),
    #
    # Children
    # --------
    #
    ("$.foo", {"foo": "bar"}, "baz", {"foo": "baz"}),
    ("foo.bar", {"foo": {"bar": 1}}, "baz", {"foo": {"bar": "baz"}}),
    #
    # Descendants
    # -----------
    #
    ("$..somefield", {"somefield": 1}, 42, {"somefield": 42}),
    (
        "$..nestedfield",
        {"outer": {"nestedfield": 1}},
        42,
        {"outer": {"nestedfield": 42}},
    ),
    (
        "$..bar",
        {"outs": {"bar": 1, "ins": {"bar": 9}}, "outs2": {"bar": 2}},
        42,
        {"outs": {"bar": 42, "ins": {"bar": 42}}, "outs2": {"bar": 42}},
    ),
    #
    # Where
    # -----
    #
    (
        "*.bar where baz",
        {"foo": {"bar": {"baz": 1}}, "bar": {"baz": 2}},
        5,
        {"foo": {"bar": 5}, "bar": {"baz": 2}},
    ),
    (
        "(* where flag) .. bar",
        {"foo": {"bar": 1, "flag": 1}, "baz": {"bar": 2}},
        3,
        {"foo": {"bar": 3, "flag": 1}, "baz": {"bar": 2}},
    ),
    #
    # WhereNot
    # --------
    #
    (
        '(* wherenot flag) .. bar',
        {'foo': {'bar': 1, 'flag': 1}, 'baz': {'bar': 2}},
        4,
        {'foo': {'bar': 1, 'flag': 1}, 'baz': {'bar': 4}},
    ),
    #
    # Lambdas
    # -------
    #
    (
        "foo[*].baz",
        {'foo': [{'baz': 1}, {'baz': 2}]},
        lambda x, y, z: x + 1,
        {'foo': [{'baz': 2}, {'baz': 3}]}
    ),
    #
    # Update with Boolean in data
    # ---------------------------
    #
    (
        "$.*.number",
        {'foo': ['abc', 'def'], 'bar': {'number': 123456}, 'boolean': True},
        '98765',
        {'foo': ['abc', 'def'], 'bar': {'number': '98765'}, 'boolean': True},
    ),
)


@pytest.mark.parametrize(
    "expression, data, update_value, expected_value",
    update_test_cases,
)
@parsers
def test_update(parse: Callable[[str], JSONPath], expression: str, data, update_value, expected_value):
    data_copy = copy.deepcopy(data)
    update_value_copy = copy.deepcopy(update_value)
    result = parse(expression).update(data_copy, update_value_copy)
    assert result == expected_value

    # inplace update testing
    data_copy2 = copy.deepcopy(data)
    update_value_copy2 = copy.deepcopy(update_value)
    datums = parse(expression).find(data_copy2)
    batch_update = isinstance(update_value, list) and len(datums) == len(update_value)
    for i, datum in enumerate(datums):
        if batch_update:
            datum.value = update_value_copy2[i]
        else:
            datum.value = update_value_copy2
        if isinstance(datum.full_path, (Root, This)): # when the type of `data` is str, int, float etc.
            data_copy2 = datum.value
    assert data_copy2 == expected_value


find_test_cases = (
    #
    # * (star)
    # --------
    #
    ("*", {"foo": 1, "baz": 2}, {1, 2}, {"foo", "baz"}),
    #
    # Fields
    # ------
    #
    ("foo", {"foo": "baz"}, ["baz"], ["foo"]),
    ("foo,baz", {"foo": 1, "baz": 2}, [1, 2], ["foo", "baz"]),
    ("@foo", {"@foo": 1}, [1], ["@foo"]),
    #
    # Roots
    # -----
    #
    ("$", {"foo": "baz"}, [{"foo": "baz"}], ["$"]),
    ("foo.$", {"foo": "baz"}, [{"foo": "baz"}], ["$"]),
    ("foo.$.foo", {"foo": "baz"}, ["baz"], ["foo"]),
    #
    # This
    # ----
    #
    ("`this`", {"foo": "baz"}, [{"foo": "baz"}], ["`this`"]),
    ("foo.`this`", {"foo": "baz"}, ["baz"], ["foo"]),
    ("foo.`this`.baz", {"foo": {"baz": 3}}, [3], ["foo.baz"]),
    #
    # Indexes
    # -------
    #
    ("[0]", [42], [42], ["[0]"]),
    ("[5]", [42], [], []),
    ("[2]", [34, 65, 29, 59], [29], ["[2]"]),
    ("[0]", None, [], []),
    #
    # Slices
    # ------
    #
    ("[*]", [1, 2, 3], [1, 2, 3], ["[0]", "[1]", "[2]"]),
    ("[*]", range(1, 4), [1, 2, 3], ["[0]", "[1]", "[2]"]),
    ("[1:]", [1, 2, 3, 4], [2, 3, 4], ["[1]", "[2]", "[3]"]),
    ("[1:3]", [1, 2, 3, 4], [2, 3], ["[1]", "[2]"]),
    ("[:2]", [1, 2, 3, 4], [1, 2], ["[0]", "[1]"]),
    ("[:3:2]", [1, 2, 3, 4], [1, 3], ["[0]", "[2]"]),
    ("[1::2]", [1, 2, 3, 4], [2, 4], ["[1]", "[3]"]),
    ("[1:6:3]", range(1, 10), [2, 5], ["[1]", "[4]"]),
    ("[::-2]", [1, 2, 3, 4, 5], [5, 3, 1], ["[4]", "[2]", "[0]"]),
    #
    # Slices (funky hacks)
    # --------------------
    #
    ("[*]", 1, [1], ["[0]"]),
    ("[0:]", 1, [1], ["[0]"]),
    ("[*]", {"foo": 1}, [{"foo": 1}], ["[0]"]),
    ("[*].foo", {"foo": 1}, [1], ["[0].foo"]),
    #
    # Children
    # --------
    #
    ("foo.baz", {"foo": {"baz": 3}}, [3], ["foo.baz"]),
    ("foo.baz", {"foo": {"baz": [3]}}, [[3]], ["foo.baz"]),
    ("foo.baz.qux", {"foo": {"baz": {"qux": 5}}}, [5], ["foo.baz.qux"]),
    #
    # Descendants
    # -----------
    #
    (
        "foo..baz",
        {"foo": {"baz": 1, "bing": {"baz": 2}}},
        [1, 2],
        ["foo.baz", "foo.bing.baz"],
    ),
    (
        "foo..baz",
        {"foo": [{"baz": 1}, {"baz": 2}]},
        [1, 2],
        ["foo.[0].baz", "foo.[1].baz"],
    ),
    #
    # Parents
    # -------
    #
    ("foo.baz.`parent`", {"foo": {"baz": 3}}, [{"baz": 3}], ["foo"]),
    (
        "foo.`parent`.foo.baz.`parent`.baz.qux",
        {"foo": {"baz": {"qux": 5}}},
        [5],
        ["foo.baz.qux"],
    ),
    #
    # Hyphens
    # -------
    #
    ("foo.bar-baz", {"foo": {"bar-baz": 3}}, [3], ["foo.bar-baz"]),
    (
        "foo.[bar-baz,blah-blah]",
        {"foo": {"bar-baz": 3, "blah-blah": 5}},
        [3, 5],
        ["foo.bar-baz", "foo.blah-blah"],
    ),
    #
    # Literals
    # --------
    #
    ("A.'a.c'", {"A": {"a.c": "d"}}, ["d"], ["A.'a.c'"]),
    #
    # Numeric keys
    # --------
    #
    ("1", {"1": "foo"}, ["foo"], ["1"]),
)


@pytest.mark.parametrize(
    "path, data, expected_values, expected_full_paths", find_test_cases
)
@parsers
def test_find(parse, path, data, expected_values, expected_full_paths):
    results = parse(path).find(data)

    # Verify result values and full paths match expectations.
    assert_value_equality(results, expected_values)
    assert_full_path_equality(results, expected_full_paths)


find_test_cases_with_auto_id = (
    #
    # * (star)
    # --------
    #
    ("*", {"foo": 1, "baz": 2}, {1, 2, "`this`"}),
    #
    # Fields
    # ------
    #
    ("foo.id", {"foo": "baz"}, ["foo"]),
    ("foo.id", {"foo": {"id": "baz"}}, ["baz"]),
    ("foo,baz.id", {"foo": 1, "baz": 2}, ["foo", "baz"]),
    ("*.id", {"foo": {"id": 1}, "baz": 2}, {"1", "baz"}),
    #
    # Roots
    # -----
    #
    ("$.id", {"foo": "baz"}, ["$"]),
    ("foo.$.id", {"foo": "baz", "id": "bizzle"}, ["bizzle"]),
    ("foo.$.baz.id", {"foo": 4, "baz": 3}, ["baz"]),
    #
    # This
    # ----
    #
    ("id", {"foo": "baz"}, ["`this`"]),
    ("foo.`this`.id", {"foo": "baz"}, ["foo"]),
    ("foo.`this`.baz.id", {"foo": {"baz": 3}}, ["foo.baz"]),
    #
    # Indexes
    # -------
    #
    ("[0].id", [42], ["[0]"]),
    ("[2].id", [34, 65, 29, 59], ["[2]"]),
    #
    # Slices
    # ------
    #
    ("[*].id", [1, 2, 3], ["[0]", "[1]", "[2]"]),
    ("[1:].id", [1, 2, 3, 4], ["[1]", "[2]", "[3]"]),
    #
    # Children
    # --------
    #
    ("foo.baz.id", {"foo": {"baz": 3}}, ["foo.baz"]),
    ("foo.baz.id", {"foo": {"baz": [3]}}, ["foo.baz"]),
    ("foo.baz.id", {"foo": {"id": "bizzle", "baz": 3}}, ["bizzle.baz"]),
    ("foo.baz.id", {"foo": {"baz": {"id": "hi"}}}, ["foo.hi"]),
    ("foo.baz.bizzle.id", {"foo": {"baz": {"bizzle": 5}}}, ["foo.baz.bizzle"]),
    #
    # Descendants
    # -----------
    #
    (
        "foo..baz.id",
        {"foo": {"baz": 1, "bing": {"baz": 2}}},
        ["foo.baz", "foo.bing.baz"],
    ),
)


@pytest.mark.parametrize("path, data, expected_values", find_test_cases_with_auto_id)
@parsers
def test_find_values_auto_id(auto_id_field, parse, path, data, expected_values):
    result = parse(path).find(data)
    assert_value_equality(result, expected_values)


@parsers
def test_find_full_paths_auto_id(auto_id_field, parse):
    results = parse("*").find({"foo": 1, "baz": 2})
    assert_full_path_equality(results, {"foo", "baz", "id"})


@pytest.mark.parametrize(
    "string, target",
    (
        ("m.[1].id", ["1.m.a2id"]),
        ("m.[1].$.b.id", ["1.bid"]),
        ("m.[0].id", ["1.m.[0]"]),
    ),
)
@parsers
def test_nested_index_auto_id(auto_id_field, parse, string, target):
    data = {
        "id": 1,
        "b": {"id": "bid", "name": "bob"},
        "m": [{"a": "a1"}, {"a": "a2", "id": "a2id"}],
    }
    result = parse(string).find(data)
    assert_value_equality(result, target)


def test_invalid_hyphenation_in_key():
    with pytest.raises(JsonPathLexerError):
        base_parse("foo.-baz")
