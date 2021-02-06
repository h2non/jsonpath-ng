from collections import namedtuple

import pytest

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
])
def test_update_create(string, initial_data, insert_val, target):
    jsonpath = parse(string)
    result = jsonpath.update(initial_data, insert_val, create=True)
    assert result == target
