#!/usr/bin/env python3

from jsonpath_ng import parse

test_cases = [
    ('$[?count(1)>2]', 'count with literal arg'),
    ('$[?count()==1]', 'count with no args'),
    ('$[?count(@..*)]', 'bare count function'),
    ('$[?length(@.a)]', 'bare length function'),
    ('$[?length()==1]', 'length with no args'),
    ('$[?length(@.a,@.b)==1]', 'length with 2 args'),
]

for selector, desc in test_cases:
    try:
        jp = parse(selector)
        print(f'✗ {desc}: Should have failed but parsed: {selector}')
    except Exception as e:
        print(f'✓ {desc}: Correctly rejected - {e}')