#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the failing array field access case
jp = parse("$[?@['0'] == 5]")
data = [[5, 6]]
result = [match.value for match in jp.find(data)]

print(f"Selector: $[?@['0'] == 5]")
print(f"Document: {data}")
print(f"Result: {result}")
print(f"Expected: []")

# Let's see what @['0'] actually evaluates to
print("\n--- Debug ---")
for i, item in enumerate(data):
    print(f"Item {i}: {item}")
    # Manually check what @['0'] would be for this item
    if hasattr(item, '__getitem__'):
        try:
            field_0 = item['0'] if isinstance(item, dict) else item[0] if isinstance(item, list) and len(item) > 0 else None
            print(f"  @['0'] would be: {field_0}")
        except (KeyError, IndexError, TypeError):
            print(f"  @['0'] would be: UNDEFINED")
    else:
        print(f"  @['0'] would be: UNDEFINED")