import copy
from collections import namedtuple
from contextlib import nullcontext as does_not_raise

import pytest

from jsonpath_ng.ext import parse

Params = namedtuple('Params', 'string initial_data insert_val target')


@pytest.mark.parametrize(
    "string, initial_data, expected_result",
    (
        ("$.foo", {}, {"foo": 42}),
        ("$.foo.bar", {}, {"foo": {"bar": 42}}),
        ("$.foo[0]", {}, {"foo": [42]}),
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


@pytest.mark.parametrize('string, initial_data, insert_val, target', [

    Params(string='$.name[0].text',
           initial_data={},
           insert_val='Sir Michael',
           target={'name': [{'text': 'Sir Michael'}]}),

    Params(string='$.name[0].given[0]',
           initial_data={'name': [{'text': 'Sir Michael'}]},
           insert_val='Michael',
           target={'name': [{'text': 'Sir Michael',
                             'given': ['Michael']}]}),

    Params(string='$.name[0].prefix[0]',
           initial_data={'name': [{'text': 'Sir Michael',
                                   'given': ['Michael']}]},
           insert_val='Sir',
           target={'name': [{'text': 'Sir Michael',
                             'given': ['Michael'],
                             'prefix': ['Sir']}]}),

    Params(string='$.birthDate',
           initial_data={'name': [{'text': 'Sir Michael',
                                   'given': ['Michael'],
                                   'prefix': ['Sir']}]},
           insert_val='1943-05-05',
           target={'name': [{'text': 'Sir Michael',
                             'given': ['Michael'],
                             'prefix': ['Sir']}],
                   'birthDate': '1943-05-05'}),
])
def test_build_doc(string, initial_data, insert_val, target):
    jsonpath = parse(string)
    result = jsonpath.update_or_create(initial_data, insert_val)
    assert result == target
