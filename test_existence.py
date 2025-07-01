#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the existence fix
selector = '$[?!@.a]'
document = [{'a': None, 'd': 'e'}, {'d': 'f'}, {'a': 'd', 'd': 'f'}]

try:
    parsed = parse(selector)
    results = [match.value for match in parsed.find(document)]
    print(f'Results: {results}')
    print(f'Expected: [{{"d": "f"}}]')
    print(f'Test passes: {results == [{"d": "f"}]}')
except Exception as e:
    print(f'Error: {e}')