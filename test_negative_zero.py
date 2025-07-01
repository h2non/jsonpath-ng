#!/usr/bin/env python3

# Test how Python handles -0
print("Testing -0 in Python:")
print(f"-0 == 0: {-0 == 0}")
print(f"-0 is 0: {-0 is 0}")
print(f"repr(-0): {repr(-0)}")
print(f"str(-0): {str(-0)}")

# The issue is that by the time the number reaches the parser,
# Python has already converted -0 to 0. I need to catch this
# at the lexer level by looking at the original string.