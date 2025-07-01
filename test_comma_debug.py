#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test cases for comma parsing
test_cases = [
    '$[0,2]',           # Basic multiple selectors
    "$['a',1]",         # Name and index
    '$[?@.a,?@.b]',     # Multiple filters
    '$[*,1]',           # Wildcard and index
]

for test in test_cases:
    try:
        result = parse(test)
        print(f'PARSED: {test} -> {result}')
    except JsonPathParserError as e:
        print(f'ERROR: {test} -> {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')