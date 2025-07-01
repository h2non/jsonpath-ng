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

# Let's test a simpler case first
print(f"\n=== Testing simpler value function ===")
simple_selector = "$[?value(@.a)=='ab']"
simple_result = [match.value for match in jp.find(document)]
print(f"$[?value(@.a)=='ab']: {simple_result}")

# Let's also test without value function
print(f"\n=== Testing without value function ===")
no_value_selector = "$[?length(@.a)>0]"
jp2 = parse(no_value_selector)
no_value_result = [match.value for match in jp2.find(document)]
print(f"$[?length(@.a)>0]: {no_value_result}")

# Manual check of what value(@.a) should return
print(f"\n=== Manual value() check ===")
for i, item in enumerate(document):
    print(f"Item {i}: {item}")
    
    # Check what @.a returns
    jp_a = parse("@.a")
    a_matches = jp_a.find(item)
    print(f"  @.a matches: {len(a_matches)}")
    if a_matches:
        print(f"  @.a values: {[m.value for m in a_matches]}")
        # value() should return the single value if exactly one match
        if len(a_matches) == 1:
            value_result = a_matches[0].value
            print(f"  value(@.a) would be: {value_result}")
            if value_result is not None:
                try:
                    length = len(value_result)
                    print(f"  length(value(@.a)) would be: {length}")
                except:
                    print(f"  length(value(@.a)) would be: UNDEFINED (no len)")
            else:
                print(f"  length(value(@.a)) would be: UNDEFINED (null)")
        else:
            print(f"  value(@.a) would be: UNDEFINED (not exactly 1 match)")
    else:
        print(f"  value(@.a) would be: UNDEFINED (no matches)")