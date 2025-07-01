#!/usr/bin/env python3

from jsonpath_ng import parse

# Test length function with literals
test_cases = [
    ('$[?length(true)>=2]', 'length(true) >= 2'),
    ('$[?length(false)>=2]', 'length(false) >= 2'), 
    ('$[?length(null)>=2]', 'length(null) >= 2'),
]

test_data = [1, 2, 3]

for selector, desc in test_cases:
    try:
        jp = parse(selector)
        result = [match.value for match in jp.find(test_data)]
        print(f'{desc}: {result} (should be [])')
    except Exception as e:
        print(f'{desc}: ERROR - {e}')