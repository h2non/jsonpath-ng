#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the failing Unicode regex
jp = parse(r"$[?match(@, '\\P{Lu}')]")
data = ['ж', 'Ж', '1', True, [], {}]
result = [match.value for match in jp.find(data)]

print(f"Selector: $[?match(@, '\\\\P{{Lu}}')]")
print(f"Document: {data}")
print(f"Result: {result}")
print(f"Expected: ['ж', '1']")

# Test what the regex pattern looks like
import re
pattern = r'\P{Lu}'
print(f"\nRegex pattern: {repr(pattern)}")

# Test each item manually
for item in data:
    if isinstance(item, str):
        try:
            match = re.search(pattern, item)
            print(f"'{item}': match={bool(match)}")
        except Exception as e:
            print(f"'{item}': error={e}")
    else:
        print(f"{item}: not a string")