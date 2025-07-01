#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the specific failing case
print("=== Match vs Search Test ===")

# Test data from the failing case
data = {'regex': 'b.?b', 'values': ['abc', 'bcd', 'bab', 'bba', 'bbab', 'b', True, [], {}]}

# Test match() - should only match ENTIRE string
jp_match = parse("$.values[?match(@, $.regex)]")
result_match = [match.value for match in jp_match.find(data)]
print(f"match() with 'b.?b': {result_match}")
print(f"Expected for match(): ['bab']")

# Test search() - should find pattern anywhere in string  
jp_search = parse("$.values[?search(@, $.regex)]")
result_search = [match.value for match in jp_search.find(data)]
print(f"search() with 'b.?b': {result_search}")
print(f"Expected for search(): ['bab', 'bba', 'bbab']")

# Manual test of the regex
import re
pattern = 'b.?b'
test_strings = ['abc', 'bcd', 'bab', 'bba', 'bbab', 'b']

print(f"\n=== Manual Regex Test ===")
print(f"Pattern: {pattern}")
for s in test_strings:
    fullmatch = bool(re.fullmatch(pattern, s))
    search = bool(re.search(pattern, s))
    print(f"'{s}': fullmatch={fullmatch}, search={search}")