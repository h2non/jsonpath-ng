#!/usr/bin/env python3

from jsonpath_ng import parse

# Valid cases that should still work
try:
    parse('$[0]')
    print('✓ Valid: $[0]')
except Exception as e:
    print(f'✗ Invalid rejection: $[0] - {e}')

try:
    parse('$.a.b')
    print('✓ Valid: $.a.b')
except Exception as e:
    print(f'✗ Invalid rejection: $.a.b - {e}')

try:
    parse('$[?count(@.*)==1]')
    print('✓ Valid: $[?count(@.*)==1]')
except Exception as e:
    print(f'✗ Invalid rejection: $[?count(@.*)==1] - {e}')

# Invalid cases that should now be caught
try:
    parse('$[?count (@.*)==1]')
    print('✗ Should have failed: $[?count (@.*)==1]')
except Exception as e:
    print(f'✓ Correctly rejected: $[?count (@.*)==1] - {e}')

try:
    parse('$. a')
    print('✗ Should have failed: $. a')
except Exception as e:
    print(f'✓ Correctly rejected: $. a - {e}')

try:
    parse('$.. a')
    print('✗ Should have failed: $.. a')
except Exception as e:
    print(f'✓ Correctly rejected: $.. a - {e}')