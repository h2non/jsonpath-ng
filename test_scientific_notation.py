#!/usr/bin/env python3

from jsonpath_ng.lexer import JsonPathLexer
from jsonpath_ng import parse

# Test scientific notation tokenization
test_cases = [
    "1e2",
    "1E2", 
    "1.5e2",
    "1.5E-2",
    "-1.5e+2"
]

lexer = JsonPathLexer()

print("=== Lexer Tests ===")
for test in test_cases:
    print(f"Testing: {test}")
    tokens = list(lexer.tokenize(test))
    for token in tokens:
        print(f"  Token: {token.type} = {token.value} ({type(token.value)})")
    print()

print("=== Parser Tests ===") 
# Test in filter context
selector_tests = [
    ('$[?@.a==1e2]', [{'a': 100, 'd': 'e'}, {'a': 100.1, 'd': 'f'}], [{'a': 100, 'd': 'e'}]),
    ('$[?@.a==1.5e2]', [{'a': 150.0, 'd': 'e'}, {'a': 150.1, 'd': 'f'}], [{'a': 150.0, 'd': 'e'}]),
]

for selector, document, expected in selector_tests:
    try:
        parsed = parse(selector)
        results = [match.value for match in parsed.find(document)]
        print(f'Selector: {selector}')
        print(f'Results: {results}')
        print(f'Expected: {expected}')
        print(f'Test passes: {results == expected}')
        print()
    except Exception as e:
        print(f'Error with {selector}: {e}')
        print()