#!/usr/bin/env python3

import re
import regex

# Test different regex flags to see if any give the expected behavior
pattern = '.'
test_chars = ['\u2028', '\u2029', '\r', '\n']

print("=== Testing different regex flags ===")

# Test various flag combinations
flag_combinations = [
    ("No flags", 0),
    ("DOTALL", re.DOTALL),
    ("UNICODE", re.UNICODE if hasattr(re, 'UNICODE') else 0),
    ("ASCII", re.ASCII if hasattr(re, 'ASCII') else 0),
]

for flag_name, flags in flag_combinations:
    print(f"\n{flag_name}:")
    for char in test_chars:
        try:
            fullmatch = bool(re.fullmatch(pattern, char, flags))
            search = bool(re.search(pattern, char, flags))
            print(f"  '{repr(char)}': fullmatch={fullmatch}, search={search}")
        except Exception as e:
            print(f"  '{repr(char)}': error={e}")

# Test with regex module flags
print(f"\n=== Testing regex module flags ===")
regex_flags = [
    ("No flags", 0),
    ("DOTALL", regex.DOTALL),
    ("ASCII", regex.ASCII),
    ("UNICODE", regex.UNICODE if hasattr(regex, 'UNICODE') else 0),
]

for flag_name, flags in regex_flags:
    print(f"\n{flag_name}:")
    for char in test_chars:
        try:
            fullmatch = bool(regex.fullmatch(pattern, char, flags))
            search = bool(regex.search(pattern, char, flags))
            print(f"  '{repr(char)}': fullmatch={fullmatch}, search={search}")
        except Exception as e:
            print(f"  '{repr(char)}': error={e}")

# Maybe we need a custom pattern that excludes \r specifically?
print(f"\n=== Testing custom patterns ===")
custom_patterns = [
    ('[^\\r\\n]', 'Exclude \\r and \\n'),
    ('[^\\x00-\\x1F\\x7F]', 'Exclude ASCII control chars'),
    ('[^\\p{Cc}]', 'Exclude Unicode control chars (regex module)'),
]

for pattern, desc in custom_patterns:
    print(f"\nPattern: {pattern} ({desc})")
    for char in test_chars:
        try:
            # Test with regex module since it supports \p{} 
            fullmatch = bool(regex.fullmatch(pattern, char))
            print(f"  '{repr(char)}': fullmatch={fullmatch}")
        except Exception as e:
            print(f"  '{repr(char)}': error={e}")