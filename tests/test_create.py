#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# NOTICE:
# modified by elrandira to support commas for index accesses and steps in slices
# https://github.com/h2non/jsonpath-ng/pull/102

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

    Params(string='$.foo[1,3]',
           initial_data={},
           insert_val=[42, 51],
           target={'foo': [{}, 42, {}, 51]}),

    Params(string='$.foo[0].bar',
           initial_data={},
           insert_val=42,
           target={'foo': [{'bar': 42}]}),

    Params(string='$.foo[1].bar',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, {'bar': 42}]}),

    # Note that each field will received the full <insert_val>
    Params(string='$.foo[1,3].bar',
           initial_data={},
           insert_val=[42, 51],
           target={'foo': [{}, {'bar': [42, 51]}, {}, {'bar': [42, 51]}]}),

    Params(string='$.foo[0][0]',
           initial_data={},
           insert_val=42,
           target={'foo': [[42]]}),

    Params(string='$.foo[1][1]',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, [{}, 42]]}),

    # But here Note that each index will received one value of <insert_val>
    Params(string='$.foo[1,3][1]',
           initial_data={},
           insert_val=[42, 51],
           target={'foo': [{}, [{}, 42], {}, [{}, 51]]}),

    Params(string='$.foo[1,3][1]',
           initial_data={},
           insert_val=[[42, 51], [42, 51]],
           target={'foo': [{}, [{}, [42, 51]], {}, [{}, [42, 51]]]}),

    Params(string='$.foo[1,3][0,2]',
           initial_data={},
           insert_val=[42, 51, 42, 51],
           target={'foo': [{}, [42, {}, 51], {}, [42, {}, 51]]}),

    Params(string='foo[0]',
           initial_data={},
           insert_val=42,
           target={'foo': [42]}),

    Params(string='foo[1]',
           initial_data={},
           insert_val=42,
           target={'foo': [{}, 42]}),

    Params(string='foo[1,3]',
           initial_data={},
           insert_val=[42, 51],
           target={'foo': [{}, 42, {}, 51]}),

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

    Params(string='[1,3]',
           initial_data=[],
           insert_val=[42, 51],
           target=[{}, 42, {}, 51]),

    # Converts initial data to a list if necessary
    Params(string='[0]',
           initial_data={},
           insert_val=42,
           target=[42]),

    Params(string='[1]',
           initial_data={},
           insert_val=42,
           target=[{}, 42]),

    Params(string='[1,3]',
           initial_data={},
           insert_val=[42, 51],
           target=[{}, 42, {}, 51]),

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

    # more indices than values to insert
    Params(string='$.foo[1,2,3]',
           initial_data={},
           insert_val=[42, 51],
           target={'foo': [{}, 42, 51, {}]}),
    # raises IndexError


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
