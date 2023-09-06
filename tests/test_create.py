import doctest
from collections import namedtuple

import pytest

import jsonpath_ng
from jsonpath_ng.ext import parse

Params = namedtuple('Params', 'string initial_data insert_val target')


@pytest.mark.parametrize('string, initial_data, insert_val, target', [

    Params(string='$.foo',
           initial_data={},
           insert_val=42,
           target={'foo': 42}),

    Params(string='$.foo.bar',
           initial_data={},
           insert_val=42,
           target={'foo': {'bar': 42}}),

    Params(string='$.foo[0]',
           initial_data={},
           insert_val=42,
           target={'foo': [42]}),

    Params(string='$.foo[1]',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, 42]}),

    Params(string='$.foo[0].bar',
           initial_data={},
           insert_val=42,
           target={'foo': [{'bar': 42}]}),

    Params(string='$.foo[1].bar',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, {'bar': 42}]}),

    Params(string='$.foo[0][0]',
           initial_data={},
           insert_val=42,
           target={'foo': [[42]]}),

    Params(string='$.foo[1][1]',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, [{}, 42]]}),

    Params(string='foo[0]',
           initial_data={},
           insert_val=42,
           target={'foo': [42]}),

    Params(string='foo[1]',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, 42]}),

    Params(string='foo',
           initial_data={},
           insert_val=42,
           target={'foo': 42}),

    # Initial data can be a list if we expect a list back
    Params(string='[0]',
           initial_data=[],
           insert_val=42,
           target=[42]),

    Params(string='[1]',
           initial_data=[],
           insert_val=42,
           target=[{}, 42]),

    # Converts initial data to a list if necessary
    Params(string='[0]',
           initial_data={},
           insert_val=42,
           target=[42]),

    Params(string='[1]',
           initial_data={},
           insert_val=42,
           target=[{}, 42]),

    Params(string='foo[?bar="baz"].qux',
           initial_data={'foo': [
               {'bar': 'baz'},
               {'bar': 'bizzle'},
           ]},
           insert_val=42,
           target={'foo': [
               {'bar': 'baz', 'qux': 42},
               {'bar': 'bizzle'}
           ]}),
])
def test_update_or_create(string, initial_data, insert_val, target):
    jsonpath = parse(string)
    result = jsonpath.update_or_create(initial_data, insert_val)
    assert result == target


@pytest.mark.parametrize('string, initial_data, insert_val, target', [
    # Slice not supported
    Params(string='foo[0:1]',
           initial_data={},
           insert_val=42,
           target={'foo': [42, 42]}),
    # result is {'foo': {}}

    # Filter does not create items to meet criteria
    Params(string='foo[?bar="baz"].qux',
           initial_data={},
           insert_val=42,
           target={'foo': [{'bar': 'baz', 'qux': 42}]}),
    # result is {'foo': {}}

    # Does not convert initial data to a dictionary
    Params(string='foo',
           initial_data=[],
           insert_val=42,
           target={'foo': 42}),
    # raises TypeError

])
@pytest.mark.xfail
def test_unsupported_classes(string, initial_data, insert_val, target):
    jsonpath = parse(string)
    result = jsonpath.update_or_create(initial_data, insert_val)
    assert result == target


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


def test_doctests():
    results = doctest.testmod(jsonpath_ng)
    assert results.failed == 0
