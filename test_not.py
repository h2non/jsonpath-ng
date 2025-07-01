#!/usr/bin/env python3

from jsonpath_ng import parse

# Test logical NOT 
selector = '$[?!(@.a==b)]'
try:
    parsed = parse(selector)
    print('SUCCESS: Parsed logical NOT selector')
    test_data = [{'a': 'a'}, {'a': 'b'}, {'a': 'c'}]
    results = [match.value for match in parsed.find(test_data)]
    print(f'Results: {results}')
    print(f'Expected: should filter out items where a==b, so should return [{{a: a}}, {{a: c}}]')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()