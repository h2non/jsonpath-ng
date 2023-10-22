# -*- coding: utf-8 -*-

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

"""
test_jsonpath_ng_ext
----------------------------------

Tests for `jsonpath_ng_ext` module.
"""

from jsonpath_ng import jsonpath  # For setting the global auto_id_field flag

from jsonpath_ng.ext import parser
from jsonpath_ng.exceptions import JsonPathParserError

import pytest


# Example from https://docs.pytest.org/en/7.1.x/example/parametrize.html#a-quick-port-of-testscenarios
def pytest_generate_tests(metafunc):
    if metafunc.cls is None:
        return
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class Testjsonpath_ng_ext:
    scenarios = [
        ('sorted_list', dict(string='objects.`sorted`',
                             data={'objects': ['alpha', 'gamma', 'beta']},
                             target=[['alpha', 'beta', 'gamma']])),
        ('sorted_list_indexed', dict(string='objects.`sorted`[1]',
                                     data={'objects': [
                                         'alpha', 'gamma', 'beta']},
                                     target='beta')),
        ('sorted_dict', dict(string='objects.`sorted`',
                             data={'objects': {'cow': 'moo', 'horse': 'neigh',
                                               'cat': 'meow'}},
                             target=[['cat', 'cow', 'horse']])),
        ('sorted_dict_indexed', dict(string='objects.`sorted`[0]',
                                     data={'objects': {'cow': 'moo',
                                                       'horse': 'neigh',
                                                       'cat': 'meow'}},
                                     target='cat')),

        ('len_list', dict(string='objects.`len`',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=3)),
        ('len_dict', dict(string='objects.`len`',
                          data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
                          target=2)),
        ('len_str', dict(string='objects[0].`len`',
                         data={'objects': ['alpha', 'gamma']},
                         target=5)),

        ('filter_list', dict(string='objects[?@="alpha"]',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=['alpha'])),
        ('filter_list_2', dict(string='objects[?@ =~ "a.+"]',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=['alpha','gamma'])),
        ('filter_list_3', dict(string='objects[?@ =~ "a.+"]',
                          data={'objects': [1, 2, 3]},
                          target=[])),

        ('keys_list', dict(string='objects.`keys`',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=[])),
        ('keys_dict', dict(string='objects.`keys`',
                          data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
                          target=['cow','cat'])),

        ('filter_exists_syntax1', dict(string='objects[?cow]',
                                       data={'objects': [{'cow': 'moo'},
                                                         {'cat': 'neigh'}]},
                                       target=[{'cow': 'moo'}])),
        ('filter_exists_syntax2', dict(string='objects[?@.cow]',
                                       data={'objects': [{'cow': 'moo'},
                                                         {'cat': 'neigh'}]},
                                       target=[{'cow': 'moo'}])),
        ('filter_exists_syntax3', dict(string='objects[?(@.cow)]',
                                       data={'objects': [{'cow': 'moo'},
                                                         {'cat': 'neigh'}]},
                                       target=[{'cow': 'moo'}])),
        ('filter_exists_syntax4', dict(string='objects[?(@."cow!?cat")]',
                                       data={'objects': [{'cow!?cat': 'moo'},
                                                         {'cat': 'neigh'}]},
                                       target=[{'cow!?cat': 'moo'}])),
        ('filter_eq1', dict(string='objects[?cow="moo"]',
                            data={'objects': [{'cow': 'moo'},
                                              {'cow': 'neigh'},
                                              {'cat': 'neigh'}]},
                            target=[{'cow': 'moo'}])),
        ('filter_eq2', dict(string='objects[?(@.["cow"]="moo")]',
                            data={'objects': [{'cow': 'moo'},
                                              {'cow': 'neigh'},
                                              {'cat': 'neigh'}]},
                            target=[{'cow': 'moo'}])),
        ('filter_eq3', dict(string='objects[?cow=="moo"]',
                            data={'objects': [{'cow': 'moo'},
                                              {'cow': 'neigh'},
                                              {'cat': 'neigh'}]},
                            target=[{'cow': 'moo'}])),
        ('filter_gt', dict(string='objects[?cow>5]',
                           data={'objects': [{'cow': 8},
                                             {'cow': 7},
                                             {'cow': 5},
                                             {'cow': 'neigh'}]},
                           target=[{'cow': 8}, {'cow': 7}])),
        ('filter_and', dict(string='objects[?cow>5&cat=2]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 7, 'cat': 2}])),
        ('filter_float_gt', dict(
            string='objects[?confidence>=0.5].prediction',
            data={
                'objects': [
                    {'confidence': 0.42,
                     'prediction': 'Good'},
                    {'confidence': 0.58,
                     'prediction': 'Bad'},
                ]
            },
            target=['Bad']
        )),
        ('sort1', dict(string='objects[/cow]',
                       data={'objects': [{'cat': 1, 'cow': 2},
                                         {'cat': 2, 'cow': 1},
                                         {'cat': 3, 'cow': 3}]},
                       target=[[{'cat': 2, 'cow': 1},
                               {'cat': 1, 'cow': 2},
                               {'cat': 3, 'cow': 3}]])),
        ('sort1_indexed', dict(string='objects[/cow][0].cat',
                               data={'objects': [{'cat': 1, 'cow': 2},
                                                 {'cat': 2, 'cow': 1},
                                                 {'cat': 3, 'cow': 3}]},
                               target=2)),
        ('sort2', dict(string='objects[\\cat]',
                       data={'objects': [{'cat': 2}, {'cat': 1}, {'cat': 3}]},
                       target=[[{'cat': 3}, {'cat': 2}, {'cat': 1}]])),
        ('sort2_indexed', dict(string='objects[\\cat][-1].cat',
                               data={'objects': [{'cat': 2}, {'cat': 1},
                                                 {'cat': 3}]},
                               target=1)),
        ('sort3', dict(string='objects[/cow,\\cat]',
                       data={'objects': [{'cat': 1, 'cow': 2},
                                         {'cat': 2, 'cow': 1},
                                         {'cat': 3, 'cow': 1},
                                         {'cat': 3, 'cow': 3}]},
                       target=[[{'cat': 3, 'cow': 1},
                               {'cat': 2, 'cow': 1},
                               {'cat': 1, 'cow': 2},
                               {'cat': 3, 'cow': 3}]])),
        ('sort3_indexed', dict(string='objects[/cow,\\cat][0].cat',
                               data={'objects': [{'cat': 1, 'cow': 2},
                                                 {'cat': 2, 'cow': 1},
                                                 {'cat': 3, 'cow': 1},
                                                 {'cat': 3, 'cow': 3}]},
                               target=3)),
        ('sort4', dict(string='objects[/cat.cow]',
                       data={'objects': [{'cat': {'dog': 1, 'cow': 2}},
                                         {'cat': {'dog': 2, 'cow': 1}},
                                         {'cat': {'dog': 3, 'cow': 3}}]},
                       target=[[{'cat': {'dog': 2, 'cow': 1}},
                               {'cat': {'dog': 1, 'cow': 2}},
                               {'cat': {'dog': 3, 'cow': 3}}]])),
        ('sort4_indexed', dict(string='objects[/cat.cow][0].cat.dog',
                               data={'objects': [{'cat': {'dog': 1,
                                                          'cow': 2}},
                                                 {'cat': {'dog': 2,
                                                          'cow': 1}},
                                                 {'cat': {'dog': 3,
                                                          'cow': 3}}]},
                               target=2)),
        ('sort5_twofields', dict(string='objects[/cat.(cow,bow)]',
                                 data={'objects':
                                       [{'cat': {'dog': 1, 'bow': 3}},
                                        {'cat': {'dog': 2, 'cow': 1}},
                                        {'cat': {'dog': 2, 'bow': 2}},
                                        {'cat': {'dog': 3, 'cow': 2}}]},
                                 target=[[{'cat': {'dog': 2, 'cow': 1}},
                                         {'cat': {'dog': 2, 'bow': 2}},
                                         {'cat': {'dog': 3, 'cow': 2}},
                                         {'cat': {'dog': 1, 'bow': 3}}]])),

        ('sort5_indexed', dict(string='objects[/cat.(cow,bow)][0].cat.dog',
                               data={'objects':
                                     [{'cat': {'dog': 1, 'bow': 3}},
                                      {'cat': {'dog': 2, 'cow': 1}},
                                      {'cat': {'dog': 2, 'bow': 2}},
                                      {'cat': {'dog': 3, 'cow': 2}}]},
                               target=2)),
        ('arithmetic_number_only', dict(string='3 * 3', data={},
                                        target=[9])),

        ('arithmetic_mul1', dict(string='$.foo * 10', data={'foo': 4},
                                 target=[40])),
        ('arithmetic_mul2', dict(string='10 * $.foo', data={'foo': 4},
                                 target=[40])),
        ('arithmetic_mul3', dict(string='$.foo * 10', data={'foo': 4},
                                 target=[40])),
        ('arithmetic_mul4', dict(string='$.foo * 3', data={'foo': 'f'},
                                 target=['fff'])),
        ('arithmetic_mul5', dict(string='foo * 3', data={'foo': 'f'},
                                 target=['foofoofoo'])),
        ('arithmetic_mul6', dict(string='($.foo * 10 * $.foo) + 2',
                                 data={'foo': 4}, target=[162])),
        ('arithmetic_mul7', dict(string='$.foo * 10 * $.foo + 2',
                                 data={'foo': 4}, target=[240])),

        ('arithmetic_str0', dict(string='foo + bar',
                                 data={'foo': 'name', "bar": "node"},
                                 target=["foobar"])),
        ('arithmetic_str1', dict(string='foo + "_" + bar',
                                 data={'foo': 'name', "bar": "node"},
                                 target=["foo_bar"])),
        ('arithmetic_str2', dict(string='$.foo + "_" + $.bar',
                                 data={'foo': 'name', "bar": "node"},
                                 target=["name_node"])),
        ('arithmetic_str3', dict(string='$.foo + $.bar',
                                 data={'foo': 'name', "bar": "node"},
                                 target=["namenode"])),
        ('arithmetic_str4', dict(string='foo.cow + bar.cow',
                                 data={'foo': {'cow': 'name'},
                                       "bar": {'cow': "node"}},
                                 target=["namenode"])),

        ('arithmetic_list1', dict(string='$.objects[*].cow * 2',
                                  data={'objects': [{'cow': 1},
                                                    {'cow': 2},
                                                    {'cow': 3}]},
                                  target=[2, 4, 6])),

        ('arithmetic_list2', dict(string='$.objects[*].cow * $.objects[*].cow',
                                  data={'objects': [{'cow': 1},
                                                    {'cow': 2},
                                                    {'cow': 3}]},
                                  target=[1, 4, 9])),

        ('arithmetic_list_err1', dict(
            string='$.objects[*].cow * $.objects2[*].cow',
            data={'objects': [{'cow': 1}, {'cow': 2}, {'cow': 3}],
                  'objects2': [{'cow': 5}]},
            target=[])),

        ('arithmetic_err1', dict(string='$.objects * "foo"',
                                 data={'objects': []}, target=[])),
        ('arithmetic_err2', dict(string='"bar" * "foo"', data={}, target=[])),

        ('real_life_example1', dict(
            string="payload.metrics[?(@.name='cpu.frequency')].value * 100",
            data={'payload': {'metrics': [
                {'timestamp': '2013-07-29T06:51:34.472416',
                 'name': 'cpu.frequency',
                 'value': 1600,
                 'source': 'libvirt.LibvirtDriver'},
                {'timestamp': '2013-07-29T06:51:34.472416',
                 'name': 'cpu.user.time',
                 'value': 17421440000000,
                 'source': 'libvirt.LibvirtDriver'}]}},
            target=[160000])),

        ('real_life_example2', dict(
            string="payload.(id|(resource.id))",
            data={'payload': {'id': 'foobar'}},
            target=['foobar'])),
        ('real_life_example3', dict(
            string="payload.id|(resource.id)",
            data={'payload': {'resource':
                              {'id': 'foobar'}}},
            target=['foobar'])),
        ('real_life_example4', dict(
            string="payload.id|(resource.id)",
            data={'payload': {'id': 'yes',
                              'resource': {'id': 'foobar'}}},
            target=['yes', 'foobar'])),

        ('sub1', dict(
            string="payload.`sub(/(foo\\\\d+)\\\\+(\\\\d+bar)/, \\\\2-\\\\1)`",
            data={'payload': "foo5+3bar"},
            target=["3bar-foo5"]
        )),
        ('sub2', dict(
            string='payload.`sub(/foo\\\\+bar/, repl)`',
            data={'payload': "foo+bar"},
            target=["repl"]
        )),
        ('str1', dict(
            string='payload.`str()`',
            data={'payload': 1},
            target=["1"]
        )),
        ('split1', dict(
            string='payload.`split(-, 2, -1)`',
            data={'payload': "foo-bar-cat-bow"},
            target=["cat"]
        )),
        ('split2', dict(
            string='payload.`split(-, 2, 2)`',
            data={'payload': "foo-bar-cat-bow"},
            target=["cat-bow"]
        )),

        ('bug-#2-correct', dict(
            string='foo[?(@.baz==1)]',
            data={'foo': [{'baz': 1}, {'baz': 2}]},
            target=[{'baz': 1}],
        )),

        ('bug-#2-wrong', dict(
            string='foo[*][?(@.baz==1)]',
            data={'foo': [{'baz': 1}, {'baz': 2}]},
            target=[],
        )),

        ('boolean-filter-true', dict(
            string='foo[?flag = true].color',
            data={'foo': [{"color": "blue", "flag": True},
                          {"color": "green", "flag": False}]},
            target=['blue']
        )),

        ('boolean-filter-false', dict(
            string='foo[?flag = false].color',
            data={'foo': [{"color": "blue", "flag": True},
                          {"color": "green", "flag": False}]},
            target=['green']
        )),

        ('boolean-filter-other-datatypes-involved', dict(
            string='foo[?flag = true].color',
            data={'foo': [{"color": "blue", "flag": True},
                          {"color": "green", "flag": 2},
                          {"color": "red", "flag": "hi"}]},
            target=['blue']
        )),

        ('boolean-filter-string-true-string-literal', dict(
            string='foo[?flag = "true"].color',
            data={'foo': [{"color": "blue", "flag": True},
                          {"color": "green", "flag": "true"}]},
            target=['green']
        )),
    ]

    def test_fields_value(self, string, data, target):
        jsonpath.auto_id_field = None
        result = parser.parse(string, debug=True).find(data)
        if isinstance(target, list):
            assert target == [r.value for r in result]
        elif isinstance(target, set):
            assert target == set([r.value for r in result])
        elif isinstance(target, (int, float)):
            assert target == result[0].value
        else:
            assert target == result[0].value


def test_invalid_hyphenation_in_key():
    # This test is almost copied-and-pasted directly from `test_jsonpath.py`.
    # However, the parsers generate different exceptions for this syntax error.
    # This discrepancy needs to be resolved.
    with pytest.raises(JsonPathParserError):
        parser.parse("foo.-baz")
