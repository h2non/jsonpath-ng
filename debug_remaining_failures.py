#!/usr/bin/env python3

import json
from jsonpath_ng import parse

# Load the test cases
with open('jsonpath-compliance-test-suite/cts.json', 'r') as f:
    tests = json.load(f)['tests']

# Find the specific failing tests by their patterns
failing_patterns = [
    "name segment on array, selects nothing",
    "arg is special nothing",
    "regex from the document", 
    "unicode char class, uppercase",
    "dot matcher on \\u2028",
    "dot matcher on \\u2029",
    "arg is a function expression"
]

for test in tests:
    if any(pattern in test['name'] for pattern in failing_patterns):
        print(f"\n=== {test['name']} ===")
        print(f"Selector: {test['selector']}")
        print(f"Document: {test['document']}")
        if 'result' in test:
            print(f"Expected: {test['result']}")
            
            try:
                jp = parse(test['selector'])
                result = [match.value for match in jp.find(test['document'])]
                print(f"Got: {result}")
                print(f"Match: {result == test['result']}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Should be invalid selector")