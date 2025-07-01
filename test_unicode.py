#!/usr/bin/env python3

from jsonpath_ng import parse

# Test the actual surrogate pair cases from the compliance tests
test_doc_1 = {'𝄞': 'A'}
jp1 = parse(r'$["\uD834\uDD1E"]')
result1 = [match.value for match in jp1.find(test_doc_1)]
print(f'Test 1 - $["\\uD834\\uDD1E"] on {test_doc_1}: {result1}')

test_doc_2 = {'😀': 'A'} 
jp2 = parse(r'$["\uD83D\uDE00"]')
result2 = [match.value for match in jp2.find(test_doc_2)]
print(f'Test 2 - $["\\uD83D\\uDE00"] on {test_doc_2}: {result2}')

test_doc_3 = {'\ud7ff\ud7ff': 'A'}
jp3 = parse(r'$["\uD7FF\uD7FF"]')
result3 = [match.value for match in jp3.find(test_doc_3)]
print(f'Test 3 - $["\\uD7FF\\uD7FF"] on {test_doc_3}: {result3}')

# Test invalid cases 
try:
    jp_invalid = parse(r'$["\uD800"]')
    print("ERROR: Should have failed for single high surrogate")
except Exception as e:
    print(f"✓ Correctly rejected single high surrogate: {e}")