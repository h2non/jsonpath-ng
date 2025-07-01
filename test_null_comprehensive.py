#!/usr/bin/env python3

from jsonpath_ng import parse

# Test comprehensive null comparison scenarios
test_cases = [
    # Missing field vs null comparison
    ('$[?@.a==null]', [{'d': 'e'}, {'a': None, 'd': 'f'}, {'a': 'c', 'd': 'g'}], [{'a': None, 'd': 'f'}]),
    
    # Missing field vs not-null comparison
    ('$[?@.a!=null]', [{'d': 'e'}, {'a': None, 'd': 'f'}, {'a': 'c', 'd': 'g'}], [{'d': 'e'}, {'a': 'c', 'd': 'g'}]),
    
    # String literal comparison should still work
    ('$[?@.a==\'c\']', [{'d': 'e'}, {'a': None, 'd': 'f'}, {'a': 'c', 'd': 'g'}], [{'a': 'c', 'd': 'g'}]),
]

for selector, document, expected in test_cases:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'Selector: {selector}')
        print(f'Results: {results}')
        print(f'Expected: {expected}')
        print(f'Test passes: {results == expected}')
        print()
    except Exception as e:
        print(f'Error with {selector}: {e}')
        print()