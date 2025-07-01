#!/usr/bin/env python3

from jsonpath_ng import parse

# Debug the value function issue
selector = "$[?length(value(@.a))>0]"
document = [{'a': 'ab'}, {'c': 'd'}, {'a': None}]

print(f"Selector: {selector}")
print(f"Document: {document}")

jp = parse(selector)
result = [match.value for match in jp.find(document)]
print(f"Result: {result}")
print("Expected: [{'a': 'ab'}]")

# Let's break this down step by step
print("\n=== Step by step debug ===")
for i, item in enumerate(document):
    print(f"\nItem {i}: {item}")
    
    # Test @.a on this item
    jp_a = parse("@.a")
    a_result = jp_a.find(item)
    print(f"  @.a: {[m.value for m in a_result]}")
    
    # Test value(@.a) on this item  
    if a_result:
        # value() should return the single value if exactly one match
        jp_value = parse("value(@.a)")
        try:
            value_result = jp_value.find(item)
            print(f"  value(@.a): {[m.value for m in value_result]}")
        except Exception as e:
            print(f"  value(@.a) error: {e}")
    else:
        print(f"  value(@.a): No matches, so value() would be UNDEFINED")
    
    # Test length(value(@.a))
    try:
        jp_length = parse("length(value(@.a))")
        length_result = jp_length.find(item)
        print(f"  length(value(@.a)): {[m.value for m in length_result]}")
    except Exception as e:
        print(f"  length(value(@.a)) error: {e}")