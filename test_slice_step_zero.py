#!/usr/bin/env python3

from jsonpath_ng import parse

# Test step 0 slice
jp = parse('$[1:2:0]')
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = [match.value for match in jp.find(data)]
print(f'$[1:2:0] on {data}: {result}')
print(f'Expected: []')
print(f'Correct: {result == []}')