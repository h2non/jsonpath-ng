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
from oslotest import base
from six import moves
import testscenarios

from jsonpath_ng.ext import parser
rest_response1={
    "items":
        [
            {
                "status": "UP",
                "kind": "compute#region",
                "description": "us-central1",
                "quotas": [
                    {"usage": 3.0, "metric": "CPUS", "limit": 72.0},
                    {"usage": 261.0, "metric": "DISKS", "limit": 40960.0},
                    {"usage": 0.0, "metric": "STATIC", "limit": 21.0},
                    {"usage": 0.0, "metric": "IN_USE", "limit": 69.0},
                    {"usage": 0.0, "metric": "SSD", "limit": 20480.0}
                ],
                "id": "1000",
                "name": "us-central1"
            },
            {
                "status": "UP",
                "kind": "compute#region",
                "description": "us-central2",
                "quotas": [
                    {"usage": 0.0, "metric": "CPUS", "limit": 72.0},
                    {"usage": 0.0, "metric": "DISKS", "limit": 40960.0},
                    {"usage": 0.0, "metric": "STATIC", "limit": 21.0},
                    {"usage": 0.0, "metric": "IN_USE", "limit": 69.0},
                    {"usage": 0.0, "metric": "SSD", "limit": 20480.0}
                ],
                "id": "1001",
                "name": "us-central2"
            },
            {
                "status": "UP",
                "kind": "compute#region",
                "description": "us-central3",
                "quotas": [
                    {"usage": 0.0, "metric": "CPUS", "limit": 90.0},
                    {"usage": 0.0, "metric": "DISKS", "limit": 2040.0},
                    {"usage": 0.0, "metric": "STATIC", "limit": 46.0},
                    {"usage": 0.0, "metric": "IN_USE", "limit": 80.0},
                    {"usage": 500.0, "metric": "SSD", "limit": 20480.0}
                ],
                "id": "1002",
                "name": "us-central3"
            }
        ]
}

class Testjsonpath_ng_ext(testscenarios.WithScenarios,
                          base.BaseTestCase):
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
        ('filter_list', dict(string='objects[?@="alpha"]',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=['alpha'])),
        ('filter_list_2', dict(string='objects[?@ ~= "a.+"]',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=['alpha','gamma'])),
        ('keys_list', dict(string='objects.`keys`',
                          data={'objects': ['alpha', 'gamma', 'beta']},
                          target=[])),
        ('len_dict', dict(string='objects.`len`',
                          data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
                          target=2)),
        ('keys_dict', dict(string='objects.`keys`',
                          data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
                          target=['cow','cat'])),
        #('filter_keys_dict', dict(string='objects.`keys`[?`this`="cow"]',
        #                  data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
        #                  target=['cow'])),
        #TODO make keys dictionaries filterable
        ('len_str', dict(string='objects[0].`len`',
                         data={'objects': ['alpha', 'gamma']},
                         target=5)),
        ('contains_filter', dict(string='objects[?id ~= "v.*[1-9]"].id',
                          data={'objects': [{'id':'vasll1'},{'id':'v2'},{'id':'vaal3'},{'id':'other'},{'id':'val'}]},
                          target=['vasll1','v2','vaal3'])),

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
        ('filter_gt_negation', dict(string='objects[?!cow<=5]',
                           data={'objects': [{'cow': 8},
                                             {'cow': 7},
                                             {'cow': 5},
                                             {'cow': 'neigh'}]},
                           target=[{'cow': 8}, {'cow': 7},{'cow':'neigh'}])),
        ('filter_and', dict(string='objects[?cow>5&cat=2]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 7, 'cat': 2}])),
        ('filter_and_demorgans', dict(string='objects[?!(cow<=5|cat!=2)]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 7, 'cat': 2}])),
        ('filter_or', dict(string='objects[?cow=8|cat=3]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 5, 'cat': 3},
                                    {'cow': 8, 'cat': 3}])),
        ('filter_or_demorgans', dict(string='objects[?!(cow!=8&cat!=3)]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 5, 'cat': 3},
                                    {'cow': 8, 'cat': 3}])),
        ('filter_or_and', dict(string='objects[?cow=8&cat=2|cat=3]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 5, 'cat': 3},
                                    {'cow': 8, 'cat': 3}])),
        ('filter_or_and_overide', dict(string='objects[?cow=8&(cat=2|cat=3)]',
                            data={'objects': [{'cow': 8, 'cat': 2},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2},
                                    {'cow': 8, 'cat': 3}])),
        ('filter_or_and', dict(string='objects[?dog=1|cat=3&cow=8]',
                            data={'objects': [{'cow': 8, 'cat': 2, 'dog':1},
                                              {'cow': 7, 'cat': 2},
                                              {'cow': 2, 'cat': 2},
                                              {'cow': 5, 'cat': 3},
                                              {'cow': 8, 'cat': 3}]},
                            target=[{'cow': 8, 'cat': 2, 'dog':1},
                                    {'cow': 8, 'cat': 3}])),
        ('filter_complex', dict(string='$.items[?((!(val==4))&(id==2))|(!((id!=1)&(id!=3)))]',
                            data={"items":[{"id":1, "val":1, "info":1},{"id":2, "val":4},{"id":2,"val":2},{"id":3,"val":3}]},
                            target=[{'info': 1, 'id': 1, 'val': 1},
                                    {'id': 2, 'val': 2},
                                    {'id': 3, 'val': 3}])),
        ('filter_complex2', dict(string="$.items[?(@.quotas[?((@.metric='SSD' & @.usage>0) | (@.metric='CPU' & @.usage>0) | (@.metric='DISKS' & @.usage>0))])]",
                            data=rest_response1,
                            target=[{'description': 'us-central1',
  'id': '1000',
  'kind': 'compute#region',
  'name': 'us-central1',
  'quotas': [{'limit': 72.0, 'metric': 'CPUS', 'usage': 3.0},
             {'limit': 40960.0, 'metric': 'DISKS', 'usage': 261.0},
             {'limit': 21.0, 'metric': 'STATIC', 'usage': 0.0},
             {'limit': 69.0, 'metric': 'IN_USE', 'usage': 0.0},
             {'limit': 20480.0, 'metric': 'SSD', 'usage': 0.0}],
  'status': 'UP'},
 {'description': 'us-central3',
  'id': '1002',
  'kind': 'compute#region',
  'name': 'us-central3',
  'quotas': [{'limit': 90.0, 'metric': 'CPUS', 'usage': 0.0},
             {'limit': 2040.0, 'metric': 'DISKS', 'usage': 0.0},
             {'limit': 46.0, 'metric': 'STATIC', 'usage': 0.0},
             {'limit': 80.0, 'metric': 'IN_USE', 'usage': 0.0},
             {'limit': 20480.0, 'metric': 'SSD', 'usage': 500.0}],
  'status': 'UP'}])),
        
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
        ('sort2', dict(string='objects[\cat]',
                       data={'objects': [{'cat': 2}, {'cat': 1}, {'cat': 3}]},
                       target=[[{'cat': 3}, {'cat': 2}, {'cat': 1}]])),
        ('sort2_indexed', dict(string='objects[\cat][-1].cat',
                               data={'objects': [{'cat': 2}, {'cat': 1},
                                                 {'cat': 3}]},
                               target=1)),
        ('sort3', dict(string='objects[/cow,\cat]',
                       data={'objects': [{'cat': 1, 'cow': 2},
                                         {'cat': 2, 'cow': 1},
                                         {'cat': 3, 'cow': 1},
                                         {'cat': 3, 'cow': 3}]},
                       target=[[{'cat': 3, 'cow': 1},
                               {'cat': 2, 'cow': 1},
                               {'cat': 1, 'cow': 2},
                               {'cat': 3, 'cow': 3}]])),
        ('sort3_indexed', dict(string='objects[/cow,\cat][0].cat',
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

    def test_fields_value(self):
        jsonpath.auto_id_field = None
        result = parser.parse(self.string, debug=True).find(self.data)
        if isinstance(self.target, list):
            self.assertEqual(self.target, [r.value for r in result])
        elif isinstance(self.target, set):
            self.assertEqual(self.target, set([r.value for r in result]))
        elif isinstance(self.target, (int, float)):
            self.assertEqual(self.target, result[0].value)
        else:
            self.assertEqual(self.target, result[0].value)

# NOTE(sileht): copy of tests/test_jsonpath.py
# to ensure we didn't break jsonpath_ng


class TestJsonPath(base.BaseTestCase):
    """Tests of the actual jsonpath functionality """

    #
    # Check that the data value returned is good
    #
    def check_cases(self, test_cases):
        # Note that just manually building an AST would avoid this dep and
        # isolate the tests, but that would suck a bit
        # Also, we coerce iterables, etc, into the desired target type

        for string, data, target in test_cases:
            print('parse("%s").find(%s) =?= %s' % (string, data, target))
            result = parser.parse(string).find(data)
            if isinstance(target, list):
                assert [r.value for r in result] == target
            elif isinstance(target, set):
                assert set([r.value for r in result]) == target
            else:
                assert result.value == target

    def test_fields_value(self):
        jsonpath.auto_id_field = None
        self.check_cases([('foo', {'foo': 'baz'}, ['baz']),
                          ('foo,baz', {'foo': 1, 'baz': 2}, [1, 2]),
                          ('@foo', {'@foo': 1}, [1]),
                          ('*', {'foo': 1, 'baz': 2}, set([1, 2]))])

        jsonpath.auto_id_field = 'id'
        self.check_cases([('*', {'foo': 1, 'baz': 2}, set([1, 2, '`this`']))])

    def test_root_value(self):
        jsonpath.auto_id_field = None
        self.check_cases([
            ('$', {'foo': 'baz'}, [{'foo': 'baz'}]),
            ('foo.$', {'foo': 'baz'}, [{'foo': 'baz'}]),
            ('foo.$.foo', {'foo': 'baz'}, ['baz']),
        ])

    def test_this_value(self):
        jsonpath.auto_id_field = None
        self.check_cases([
            ('`this`', {'foo': 'baz'}, [{'foo': 'baz'}]),
            ('foo.`this`', {'foo': 'baz'}, ['baz']),
            ('foo.`this`.baz', {'foo': {'baz': 3}}, [3]),
        ])

    def test_index_value(self):
        self.check_cases([
            ('[0]', [42], [42]),
            ('[5]', [42], []),
            ('[2]', [34, 65, 29, 59], [29])
        ])

    def test_slice_value(self):
        self.check_cases([('[*]', [1, 2, 3], [1, 2, 3]),
                          ('[*]', moves.range(1, 4), [1, 2, 3]),
                          ('[1:]', [1, 2, 3, 4], [2, 3, 4]),
                          ('[:2]', [1, 2, 3, 4], [1, 2])])

        # Funky slice hacks
        self.check_cases([
            ('[*]', 1, [1]),  # This is a funky hack
            ('[0:]', 1, [1]),  # This is a funky hack
            ('[*]', {'foo': 1}, [{'foo': 1}]),  # This is a funky hack
            ('[*].foo', {'foo': 1}, [1]),  # This is a funky hack
        ])

    def test_child_value(self):
        self.check_cases([('foo.baz', {'foo': {'baz': 3}}, [3]),
                          ('foo.baz', {'foo': {'baz': [3]}}, [[3]]),
                          ('foo.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}},
                           [5])])

    def test_descendants_value(self):
        self.check_cases([
            ('foo..baz', {'foo': {'baz': 1, 'bing': {'baz': 2}}}, [1, 2]),
            ('foo..baz', {'foo': [{'baz': 1}, {'baz': 2}]}, [1, 2]),
        ])

    def test_parent_value(self):
        self.check_cases([('foo.baz.`parent`', {'foo': {'baz': 3}},
                           [{'baz': 3}]),
                          ('foo.`parent`.foo.baz.`parent`.baz.bizzle',
                           {'foo': {'baz': {'bizzle': 5}}}, [5])])

    def test_hyphen_key(self):
        # NOTE(sileht): hyphen is now a operator
        # so to use it has key we must escape it with quote
        # self.check_cases([('foo.bar-baz', {'foo': {'bar-baz': 3}}, [3]),
        #                  ('foo.[bar-baz,blah-blah]',
        #                   {'foo': {'bar-baz': 3, 'blah-blah': 5}},
        #                   [3, 5])])
        self.check_cases([('foo."bar-baz"', {'foo': {'bar-baz': 3}}, [3]),
                          ('foo.["bar-baz","blah-blah"]',
                           {'foo': {'bar-baz': 3, 'blah-blah': 5}},
                           [3, 5])])
        # self.assertRaises(lexer.JsonPathLexerError, self.check_cases,
        #                  [('foo.-baz', {'foo': {'-baz': 8}}, [8])])

    #
    # Check that the paths for the data are correct.
    # FIXME: merge these tests with the above, since the inputs are the same
    # anyhow
    #
    def check_paths(self, test_cases):
        # Note that just manually building an AST would avoid this dep and
        # isolate the tests, but that would suck a bit
        # Also, we coerce iterables, etc, into the desired target type

        for string, data, target in test_cases:
            print('parse("%s").find(%s).paths =?= %s' % (string, data, target))
            result = parser.parse(string).find(data)
            if isinstance(target, list):
                assert [str(r.full_path) for r in result] == target
            elif isinstance(target, set):
                assert set([str(r.full_path) for r in result]) == target
            else:
                assert str(result.path) == target

    def test_fields_paths(self):
        jsonpath.auto_id_field = None
        self.check_paths([('foo', {'foo': 'baz'}, ['foo']),
                          ('foo,baz', {'foo': 1, 'baz': 2}, ['foo', 'baz']),
                          ('*', {'foo': 1, 'baz': 2}, set(['foo', 'baz']))])

        jsonpath.auto_id_field = 'id'
        self.check_paths([('*', {'foo': 1, 'baz': 2},
                           set(['foo', 'baz', 'id']))])

    def test_root_paths(self):
        jsonpath.auto_id_field = None
        self.check_paths([
            ('$', {'foo': 'baz'}, ['$']),
            ('foo.$', {'foo': 'baz'}, ['$']),
            ('foo.$.foo', {'foo': 'baz'}, ['foo']),
        ])

    def test_this_paths(self):
        jsonpath.auto_id_field = None
        self.check_paths([
            ('`this`', {'foo': 'baz'}, ['`this`']),
            ('foo.`this`', {'foo': 'baz'}, ['foo']),
            ('foo.`this`.baz', {'foo': {'baz': 3}}, ['foo.baz']),
        ])

    def test_index_paths(self):
        self.check_paths([('[0]', [42], ['[0]']),
                          ('[2]', [34, 65, 29, 59], ['[2]'])])

    def test_slice_paths(self):
        self.check_paths([('[*]', [1, 2, 3], ['[0]', '[1]', '[2]']),
                          ('[1:]', [1, 2, 3, 4], ['[1]', '[2]', '[3]'])])

    def test_child_paths(self):
        self.check_paths([('foo.baz', {'foo': {'baz': 3}}, ['foo.baz']),
                          ('foo.baz', {'foo': {'baz': [3]}}, ['foo.baz']),
                          ('foo.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}},
                           ['foo.baz.bizzle'])])

    def test_descendants_paths(self):
        self.check_paths([('foo..baz', {'foo': {'baz': 1, 'bing': {'baz': 2}}},
                           ['foo.baz', 'foo.bing.baz'])])

    #
    # Check the "auto_id_field" feature
    #
    def test_fields_auto_id(self):
        jsonpath.auto_id_field = "id"
        self.check_cases([('foo.id', {'foo': 'baz'}, ['foo']),
                          ('foo.id', {'foo': {'id': 'baz'}}, ['baz']),
                          ('foo,baz.id', {'foo': 1, 'baz': 2}, ['foo', 'baz']),
                          ('*.id',
                           {'foo': {'id': 1},
                            'baz': 2},
                           set(['1', 'baz']))])

    def test_root_auto_id(self):
        jsonpath.auto_id_field = 'id'
        self.check_cases([
            ('$.id', {'foo': 'baz'}, ['$']),  # This is a wonky case that is
                                              # not that interesting
            ('foo.$.id', {'foo': 'baz', 'id': 'bizzle'}, ['bizzle']),
            ('foo.$.baz.id', {'foo': 4, 'baz': 3}, ['baz']),
        ])

    def test_this_auto_id(self):
        jsonpath.auto_id_field = 'id'
        self.check_cases([
            ('id', {'foo': 'baz'}, ['`this`']),  # This is, again, a wonky case
                                                 # that is not that interesting
            ('foo.`this`.id', {'foo': 'baz'}, ['foo']),
            ('foo.`this`.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
        ])

    def test_index_auto_id(self):
        jsonpath.auto_id_field = "id"
        self.check_cases([('[0].id', [42], ['[0]']),
                          ('[2].id', [34, 65, 29, 59], ['[2]'])])

    def test_slice_auto_id(self):
        jsonpath.auto_id_field = "id"
        self.check_cases([('[*].id', [1, 2, 3], ['[0]', '[1]', '[2]']),
                          ('[1:].id', [1, 2, 3, 4], ['[1]', '[2]', '[3]'])])

    def test_child_auto_id(self):
        jsonpath.auto_id_field = "id"
        self.check_cases([('foo.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
                          ('foo.baz.id', {'foo': {'baz': [3]}}, ['foo.baz']),
                          ('foo.baz.id', {'foo': {'id': 'bizzle', 'baz': 3}},
                           ['bizzle.baz']),
                          ('foo.baz.id', {'foo': {'baz': {'id': 'hi'}}},
                           ['foo.hi']),
                          ('foo.baz.bizzle.id',
                           {'foo': {'baz': {'bizzle': 5}}},
                           ['foo.baz.bizzle'])])

    def test_descendants_auto_id(self):
        jsonpath.auto_id_field = "id"
        self.check_cases([('foo..baz.id',
                           {'foo': {
                               'baz': 1,
                               'bing': {
                                   'baz': 2
                               }
                           }},
                           ['foo.baz',
                            'foo.bing.baz'])])
