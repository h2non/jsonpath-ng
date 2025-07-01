#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

# Test cases for validation
test_cases = [
    '$[?@.*]',  # Should be valid (existence test)
    '$[?$.*.a]',  # Should be valid (existence test)  
    '$[?@[*]==0]',  # Should be invalid (wildcard in comparison)
    '$[?@.*==0]',  # Should be invalid (wildcard in comparison)
]

for test in test_cases:
    try:
        result = parse(test)
        print(f'PARSED: {test} -> {result}')
    except JsonPathParserError as e:
        print(f'ERROR: {test} -> {e}')
    except Exception as e:
        print(f'UNEXPECTED: {test} -> {e}')