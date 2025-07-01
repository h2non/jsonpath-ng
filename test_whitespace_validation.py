#!/usr/bin/env python3

# Test some whitespace cases that should fail
from jsonpath_ng import parse

test_cases = [
    ('$[?value(@.a)]', 'bare value function'),
    ('$[?count (@.*)==1]', 'space between function name and parenthesis'),
    ('$. a', 'space between dot and name'),
]

for selector, desc in test_cases:
    try:
        jp = parse(selector)
        print(f'ERROR: {desc} should have failed: {selector}')
    except Exception as e:
        print(f'GOOD: {desc} correctly rejected: {e}')