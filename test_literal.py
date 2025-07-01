#!/usr/bin/env python3

test_string = "'a.*'"
print(f'String: {test_string}')
print('Starts with single quote:', test_string.startswith("'"))
print('Ends with single quote:', test_string.endswith("'"))
print('Without quotes:', test_string[1:-1])

# Test the exact condition
single_quoted = test_string.startswith("'") and test_string.endswith("'")
double_quoted = test_string.startswith('"') and test_string.endswith('"')

if single_quoted or double_quoted:
    print("Would be treated as literal")
else:
    print("Would be treated as field")