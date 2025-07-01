#!/usr/bin/env python3

from jsonpath_ng import parse

# Test that object field access still works
jp = parse("$[?@['a'] == 5]")
data = [{'a': 5}, {'b': 6}]
result = [match.value for match in jp.find(data)]
print(f'Object field access: {result}')  # Should be [{'a': 5}]

# Test that array index access still works 
jp2 = parse("$[?@[0] == 5]")
data2 = [[5, 6], [7, 8]]
result2 = [match.value for match in jp2.find(data2)]
print(f'Array index access: {result2}')  # Should be [[5, 6]]

# Test the multi-selector case
jp3 = parse("$[?count(@['a','d'])>1]")
data3 = [{'a': [1, 2, 3]}, {'a': [1], 'd': 'f'}, {'a': 1, 'd': 'f'}]
result3 = [match.value for match in jp3.find(data3)]
print(f'Multi-selector field access: {result3}')  # Should include last two items