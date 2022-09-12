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
# modified by elrandira to support commas for index accesses
# https://github.com/h2non/jsonpath-ng/pull/102

from __future__ import unicode_literals, print_function, absolute_import, division, generators, nested_scopes
import unittest

from jsonpath_ng.lexer import JsonPathLexer
from jsonpath_ng.parser import JsonPathParser
from jsonpath_ng.jsonpath import *

class TestParser(unittest.TestCase):
    # TODO: This will be much more effective with a few regression tests and `arbitrary` parse . pretty testing

    @classmethod
    def setup_class(cls):
        logging.basicConfig()

    def check_parse_cases(self, test_cases):
        parser = JsonPathParser(debug=True, lexer_class=lambda:JsonPathLexer(debug=False)) # Note that just manually passing token streams avoids this dep, but that sucks

        for string, parsed in test_cases:
            print(string, '=?=', parsed) # pytest captures this and we see it only on a failure, for debugging
            assert parser.parse(string) == parsed

    def test_atomic(self):
        self.check_parse_cases([('foo', Fields('foo')),
                                ('*', Fields('*')),
                                ('baz,bizzle', Fields('baz','bizzle')),
                                ('[1]', Index(1)),
                                ('[0,2,3]', Index(0,2,3)),
                                ('[1:]', Slice(start=1)),
                                ('[:]', Slice()),
                                ('[*]', Slice()),
                                ('[:2]', Slice(end=2)),
                                ('[1:2]', Slice(start=1, end=2)),
                                ('[5:-2]', Slice(start=5, end=-2))
                               ])

    def test_nested(self):
        self.check_parse_cases([('foo.baz', Child(Fields('foo'), Fields('baz'))),
                                ('foo.baz,bizzle', Child(Fields('foo'), Fields('baz', 'bizzle'))),
                                ('foo where baz', Where(Fields('foo'), Fields('baz'))),
                                ('foo..baz', Descendants(Fields('foo'), Fields('baz'))),
                                ('foo..baz.bing', Descendants(Fields('foo'), Child(Fields('baz'), Fields('bing'))))])
