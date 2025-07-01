#!/usr/bin/env python3

# Let's understand the difference between these selectors:
from jsonpath_ng import parse

data = [[5, 6]]

# @[0] - numeric index (should work)
try:
    jp1 = parse('$[?@[0] == 5]')
    result1 = [match.value for match in jp1.find(data)]
    print(f'@[0]: {result1}')
except Exception as e:
    print(f'@[0] error: {e}')

# @['0'] - string field (should not work on arrays?)
try:
    jp2 = parse("$[?@['0'] == 5]")
    result2 = [match.value for match in jp2.find(data)]
    print(f"@['0']: {result2}")
except Exception as e:
    print(f"@['0'] error: {e}")

# Let's also test on objects
obj_data = [{'0': 5, 'a': 6}]

try:
    jp3 = parse("$[?@['0'] == 5]")
    result3 = [match.value for match in jp3.find(obj_data)]
    print(f"Object @['0']: {result3}")
except Exception as e:
    print(f"Object @['0'] error: {e}")