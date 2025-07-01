#\!/usr/bin/env python3

from jsonpath_ng import parse

# Test the value function with multi-value nodelist
jp = parse('$[?value(@.*)==4]')
data = [[4, 4], {'foo': 4, 'bar': 4}]
result = [match.value for match in jp.find(data)]

print(f"Selector: $[?value(@.*)==4]")
print(f"Document: {data}")
print(f"Result: {result}")
print(f"Expected: []")
print(f"Match: {result == []}")

# Let's also test what @.* returns for each element
print("\n--- Debug @.* for each element ---")
for i, item in enumerate(data):
    print(f"Item {i}: {item}")
    jp_debug = parse('@.*')
    matches = jp_debug.find(item)
    print(f"  @.* matches: {[m.value for m in matches]}")
    print(f"  Count: {len(matches)}")
EOF < /dev/null