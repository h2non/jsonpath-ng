#!/usr/bin/env python3

from jsonpath_ng import parse

# Parse and examine the result structure
jp = parse(r'$["\uD834\uDD1E"]')

print(f"Parsed JSONPath type: {type(jp)}")
print(f"Parsed JSONPath: {jp}")

# Check the structure 
if hasattr(jp, 'left') and hasattr(jp, 'right'):
    print(f"Left: {jp.left} (type: {type(jp.left)})")
    print(f"Right: {jp.right} (type: {type(jp.right)})")
    
    if hasattr(jp.right, 'fields'):
        print(f"Right fields: {jp.right.fields}")
        for i, field in enumerate(jp.right.fields):
            print(f"  Field {i}: {repr(field)}")
            print(f"    Type: {type(field)}")
            print(f"    Length: {len(field)}")
            print(f"    Codepoints: {[hex(ord(c)) for c in field]}")

# Test with the document
test_doc = {'𝄞': 'A'}
print(f"\nDocument: {test_doc}")
print(f"Document keys: {[repr(k) for k in test_doc.keys()]}")

result = jp.find(test_doc)
print(f"Find result: {result}")

# Let's also test manually
if hasattr(jp.right, 'fields') and jp.right.fields:
    test_key = jp.right.fields[0]
    print(f"\nManual key lookup:")
    print(f"Looking for key: {repr(test_key)}")
    print(f"Key in document? {test_key in test_doc}")
    
    if test_key in test_doc:
        print(f"Value: {test_doc[test_key]}")
    else:
        print("Key not found")
        # Check if any key matches by codepoint comparison
        for doc_key in test_doc.keys():
            print(f"  Comparing with {repr(doc_key)}: codepoints {[hex(ord(c)) for c in doc_key]}")
            if doc_key == test_key:
                print(f"    MATCH!")
            else:
                print(f"    No match")