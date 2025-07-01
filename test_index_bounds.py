#!/usr/bin/env python3

from jsonpath_ng import parse

# Test index bounds handling
document = ['first', 'second']

test_cases = [
    ('$[0]', [document[0]]),     # Valid positive index
    ('$[1]', [document[1]]),     # Valid positive index
    ('$[2]', []),                # Out of bounds positive
    ('$[-1]', [document[-1]]),   # Valid negative index
    ('$[-2]', [document[-2]]),   # Valid negative index
    ('$[-3]', []),               # Out of bounds negative
    ('$[-9007199254740991]', []), # Very negative index
]

for selector, expected in test_cases:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'{selector}: {results} (expected: {expected})')
        print(f'  Test passes: {results == expected}')
    except Exception as e:
        print(f'{selector}: Error - {e}')
    print()