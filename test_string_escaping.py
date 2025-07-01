#!/usr/bin/env python3

from jsonpath_ng import parse
from jsonpath_ng.lexer import JsonPathLexer

# Test string literal escaping
test_cases = [
    ('$[?@ == "quoted\' literal"]', 'Single quote in double quotes'),
    ('$[?@ == \'quoted" literal\']', 'Double quote in single quotes'),
    ('$[?@ == "quoted\\" literal"]', 'Escaped double quote in double quotes'),
    ('$[?@ == \'quoted\\\' literal\']', 'Escaped single quote in single quotes'),
]

lexer = JsonPathLexer()

for selector, description in test_cases:
    print(f'Testing: {selector} ({description})')
    
    # Test lexer tokenization
    tokens = list(lexer.tokenize(selector))
    for token in tokens:
        if token.type == 'STRING':
            print(f'  STRING token: "{token.value}"')
    
    # Test parsing
    try:
        parsed = parse(selector)
        print(f'  Parsed successfully: {parsed}')
    except Exception as e:
        print(f'  Parse error: {e}')
    
    print()