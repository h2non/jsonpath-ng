#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the not-equals null behavior
selector = '$[?@.a!=null]'
document = [{'d': 'e'}, {'a': 'c', 'd': 'f'}]

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Results: {results}')
    print(f'Expected: [{{"d": "e"}}, {{"a": "c", "d": "f"}}]')
    print(f'Test passes: {results == [{"d": "e"}, {"a": "c", "d": "f"}]}')
    
except Exception as e:
    print(f'Error: {e}')