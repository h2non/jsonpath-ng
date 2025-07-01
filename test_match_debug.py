#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the failing match function
jp = parse("$[?match(@.a, 'a.*')]")
data = [{'a': 'ab'}]
result = [match.value for match in jp.find(data)]

print(f"Selector: $[?match(@.a, 'a.*')]")
print(f"Document: {data}")
print(f"Result: {result}")
print(f"Expected: [{{'a': 'ab'}}]")
print(f"Match: {result == [{'a': 'ab'}]}")

# Let's debug step by step
print("\n--- Debug ---")
matches = jp.find(data)
print(f"Full matches: {matches}")
for i, match in enumerate(matches):
    print(f"Match {i}: value={match.value}, path={match.path}")