#!/usr/bin/env python3

# Create a simple test to see if the function call rules are being matched

class TestParser:
    def __init__(self):
        pass
        
    def debug_match(self):
        # Test the exact pattern we expect
        tokens = ['ID', '(', 'CURRENT', '.', 'ID', ',', 'ID', ')']
        print("Token sequence for function call:")
        print(" ".join(tokens))
        
        # The rule should be: ID '(' filter_expr ',' filter_expr ')'
        # Where filter_expr can be: CURRENT '.' ID or ID
        
        print("\nExpected grammar match:")
        print("ID '(' filter_expr ',' filter_expr ')'")
        print("where filter_expr := CURRENT '.' ID | ID")
        
        print("\nActual tokens:")
        print("match ( @ . a , 'a.*' )")
        print("ID    ( CURRENT . ID , ID )")

if __name__ == "__main__":
    parser = TestParser()
    parser.debug_match()