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

import pytest

from jsonpath_ng.ext.filter import Filter, Expression
from jsonpath_ng.ext import parse
from jsonpath_ng.jsonpath import *


@pytest.mark.parametrize('string, parsed', [
    # The authors of all books in the store
    ("$.store.book[*].author",
     Child(Child(Child(Child(Root(), Fields('store')), Fields('book')),
                 Slice()), Fields('author'))),

    # All authors
    ("$..author", Descendants(Root(), Fields('author'))),

    # All things in the store
    ("$.store.*", Child(Child(Root(), Fields('store')), Fields('*'))),

    # The price of everything in the store
    ("$.store..price",
     Descendants(Child(Root(), Fields('store')), Fields('price'))),

    # The third book
    ("$..book[2]",
     Child(Descendants(Root(), Fields('book')),Index(2))),

    # The last book in order
    # ("$..book[(@.length-1)]",  # Not implemented
    #  Child(Descendants(Root(), Fields('book')), Slice(start=-1))),
    ("$..book[-1:]",
     Child(Descendants(Root(), Fields('book')), Slice(start=-1))),

    # The first two books
    ("$..book[0,1]",
     Child(Descendants(Root(), Fields('book')), Index(0,1))),

    ("$..book[:2]",
     Child(Descendants(Root(), Fields('book')), Slice(end=2))),

    # Filter all books with ISBN number
    ("$..book[?(@.isbn)]",
     Child(Descendants(Root(), Fields('book')),
           Filter([Expression(Child(This(), Fields('isbn')), None, None)]))),

    # Filter all books cheaper than 10
    ("$..book[?(@.price<10)]",
     Child(Descendants(Root(), Fields('book')),
           Filter([Expression(Child(This(), Fields('price')), '<', 10)]))),

    # All members of JSON structure
    ("$..*", Descendants(Root(), Fields('*'))),
])
def test_goessner_examples(string, parsed):
    """
    Test Stefan Goessner's `examples`_

    .. _examples: https://goessner.net/articles/JsonPath/index.html#e3
    """
    assert parse(string, debug=True) == parsed


@pytest.mark.parametrize('string, parsed', [
    # Navigate objects
    ("$.store.book[0].title",
     Child(Child(Child(Child(Root(), Fields('store')), Fields('book')),
                 Index(0)), Fields('title'))),

    # Navigate dictionaries
    ("$['store']['book'][0]['title']",
     Child(Child(Child(Child(Root(), Fields('store')), Fields('book')),
                 Index(0)), Fields('title'))),
])
def test_obj_v_dict(string, parsed):
    assert parse(string, debug=True) == parsed
