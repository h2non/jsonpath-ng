#!/usr/bin/env python3

from jsonpath_ng import parse
import re
import regex

# Test the dot pattern matching issue
test_cases = [
    ("$[?match(@, '.')]", ['\u2028', '\r', '\n', True, [], {}], ['\u2028']),
    ("$[?match(@, '.')]", ['\u2029', '\r', '\n', True, [], {}], ['\u2029']),
    ("$[?search(@, '.')]", ['\u2028', '\r\u2028\n', '\r', '\n', True, [], {}], ['\u2028', '\r\u2028\n']),
    ("$[?search(@, '.')]", ['\u2029', '\r\u2029\n', '\r', '\n', True, [], {}], ['\u2029', '\r\u2029\n'])
]

for selector, document, expected in test_cases:
    print(f"\n=== Test Case ===")
    print(f"Selector: {selector}")
    print(f"Document: {document}")
    print(f"Expected: {expected}")
    
    jp = parse(selector)
    result = [match.value for match in jp.find(document)]
    print(f"Got: {result}")
    print(f"Match: {result == expected}")

# Let's test the regex behavior manually
print(f"\n=== Manual Regex Testing ===")
pattern = '.'
test_chars = ['\u2028', '\u2029', '\r', '\n']

print("Using standard re module:")
for char in test_chars:
    fullmatch = bool(re.fullmatch(pattern, char))
    search = bool(re.search(pattern, char))
    print(f"  '{repr(char)}': fullmatch={fullmatch}, search={search}")

print("\nUsing regex module:")
for char in test_chars:
    fullmatch = bool(regex.fullmatch(pattern, char))
    search = bool(regex.search(pattern, char))
    print(f"  '{repr(char)}': fullmatch={fullmatch}, search={search}")

import unicodedata

# Check Unicode properties
print(f"\n=== Unicode Character Info ===")
for char in test_chars:
    print(f"'{repr(char)}': ord={ord(char)}, category={unicodedata.category(char) if char else 'N/A'}")