import sys
import logging

import ply.lex

from jsonpath_ng.exceptions import JsonPathLexerError

logger = logging.getLogger(__name__)


class JsonPathLexer:
    '''
    A Lexical analyzer for JsonPath.
    '''

    def __init__(self, debug=False):
        self.debug = debug
        if self.__doc__ is None:
            raise JsonPathLexerError('Docstrings have been removed! By design of PLY, jsonpath-rw requires docstrings. You must not use PYTHONOPTIMIZE=2 or python -OO.')

    def tokenize(self, string):
        '''
        Maps a string to an iterator over tokens. In other words: [char] -> [token]
        '''

        new_lexer = ply.lex.lex(module=self, debug=self.debug, errorlog=logger)
        new_lexer.latest_newline = 0
        new_lexer.string_value = None
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None:
                break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

        if new_lexer.string_value is not None:
            raise JsonPathLexerError('Unexpected EOF in string literal or identifier')

    # ============== PLY Lexer specification ==================
    #
    # This probably should be private but:
    #   - the parser requires access to `tokens` (perhaps they should be defined in a third, shared dependency)
    #   - things like `literals` might be a legitimate part of the public interface.
    #
    # Anyhow, it is pythonic to give some rope to hang oneself with :-)

    literals = ['*', '.', '[', ']', '(', ')', '$', ',', ':', '|', '&', '~', '?', '!']

    reserved_words = {
        'where': 'WHERE',
        'wherenot': 'WHERENOT',
        'null': 'NULL',
        'true': 'TRUE', 
        'false': 'FALSE',
    }

    tokens = ['DOUBLEDOT', 'NUMBER', 'ID', 'STRING', 'NAMED_OPERATOR', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR', 'CURRENT'] + list(reserved_words.values())

    states = [ ('singlequote', 'exclusive'),
               ('doublequote', 'exclusive'),
               ('backquote', 'exclusive') ]

    # Normal lexing, rather easy
    t_DOUBLEDOT = r'\.\.'
    t_EQ = r'=='
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_CURRENT = r'@'
    t_ignore = ' \t\r\n'  # Back to ignoring whitespace globally for now

    def t_ID(self, t):
        # Support broad Unicode range for identifiers per JSONPath RFC 9535
        # Start char: Letter, underscore, or unicode symbols/pictographs
        # Continue chars: Letter, number, underscore, hyphen, or unicode symbols/pictographs  
        r'([a-zA-Z_]|[\u00A0-\uFFFF]|[\U00010000-\U0001FFFF])([a-zA-Z0-9_\-]|[\u00A0-\uFFFF]|[\U00010000-\U0001FFFF])*'
        t.type = self.reserved_words.get(t.value, 'ID')
        return t

    def t_NUMBER(self, t):
        # JSON-compliant number format: no leading zeros (except for 0), no trailing decimal point
        r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'
        
        # Store original string to check for -0
        original_str = t.value
        
        try:
            # Try to parse as integer first, then float
            if '.' in t.value or 'e' in t.value.lower():
                t.value = float(t.value)
            else:
                t.value = int(t.value)
                
            # Store original string as an attribute for negative zero detection
            t.original_str = original_str
                
        except ValueError:
            # If parsing fails, treat as 0
            t.value = 0
            t.original_str = original_str
        return t



    # Single-quoted strings
    t_singlequote_ignore = ''
    def t_singlequote(self, t):
        r"'"
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string_value = ''
        t.lexer.push_state('singlequote')

    def t_singlequote_content(self, t):
        r"[^'\\]+"
        # Check for control characters (U+0000 to U+001F)
        for char in t.value:
            if ord(char) <= 0x1F:
                raise JsonPathLexerError(f'Control character U+{ord(char):04X} is not allowed in string literals')
        t.lexer.string_value += t.value

    # Unicode escapes need to be first to have higher precedence than regular escapes
    def t_singlequote_unicode(self, t):
        r'\\u[0-9a-fA-F]{4}'
        hex_digits = t.value[2:6]
        try:
            code_point = int(hex_digits, 16)
            
            # Handle UTF-16 surrogate pairs - we need to look ahead for potential pairs
            if 0xD800 <= code_point <= 0xDBFF:  # High surrogate
                # Look ahead for potential low surrogate
                remaining_input = t.lexer.lexdata[t.lexer.lexpos:]
                import re
                low_surrogate_match = re.match(r'\\u[0-9a-fA-F]{4}', remaining_input)
                if low_surrogate_match:
                    low_hex = low_surrogate_match.group()[2:]
                    low_code_point = int(low_hex, 16)
                    if 0xDC00 <= low_code_point <= 0xDFFF:  # Valid low surrogate
                        # Combine high and low surrogate
                        combined_code_point = 0x10000 + ((code_point - 0xD800) << 10) + (low_code_point - 0xDC00)
                        unicode_char = chr(combined_code_point)
                        # Advance the lexer position past the low surrogate
                        t.lexer.lexpos += len(low_surrogate_match.group())
                    else:
                        # High surrogate followed by invalid low surrogate
                        raise JsonPathLexerError(f'Invalid surrogate sequence: high surrogate U+{code_point:04X} followed by non-low-surrogate U+{low_code_point:04X}')
                else:
                    # High surrogate not followed by unicode escape - invalid
                    raise JsonPathLexerError(f'Invalid surrogate sequence: unpaired high surrogate U+{code_point:04X}')
            elif 0xDC00 <= code_point <= 0xDFFF:  # Low surrogate without high surrogate
                raise JsonPathLexerError(f'Invalid surrogate sequence: unpaired low surrogate U+{code_point:04X}')
            else:
                # Regular BMP character
                unicode_char = chr(code_point)
            
            # Check if it's a control character that should be rejected
            if ord(unicode_char) <= 0x1F:
                raise JsonPathLexerError(f'Control character U+{ord(unicode_char):04X} is not allowed in string literals')
            t.lexer.string_value += unicode_char
        except ValueError:
            raise JsonPathLexerError(f'Invalid unicode escape sequence {t.value}')

    def t_singlequote_escape(self, t):
        r'\\.'
        escaped_char = t.value[1]
        escape_map = {
            "'": "'",
            '\\': '\\',
            '/': '/',
            'b': '\b',
            'f': '\f',
            'n': '\n',
            'r': '\r',
            't': '\t'
        }
        
        if escaped_char in escape_map:
            t.lexer.string_value += escape_map[escaped_char]
        else:
            raise JsonPathLexerError(f'Invalid escape sequence \\{escaped_char} in string literal')

    def t_singlequote_end(self, t):
        r"'"
        t.value = t.lexer.string_value
        t.type = 'STRING'  # Quoted strings are string literals
        t.lexer.string_value = None
        t.lexer.pop_state()
        return t

    def t_singlequote_error(self, t):
        raise JsonPathLexerError('Error on line %s, col %s while lexing singlequoted field: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))


    # Double-quoted strings
    t_doublequote_ignore = ''
    def t_doublequote(self, t):
        r'"'
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string_value = ''
        t.lexer.push_state('doublequote')

    def t_doublequote_content(self, t):
        r'[^"\\]+'
        # Check for control characters (U+0000 to U+001F)
        for char in t.value:
            if ord(char) <= 0x1F:
                raise JsonPathLexerError(f'Control character U+{ord(char):04X} is not allowed in string literals')
        t.lexer.string_value += t.value

    # Unicode escapes need to be first to have higher precedence than regular escapes
    def t_doublequote_unicode(self, t):
        r'\\u[0-9a-fA-F]{4}'
        hex_digits = t.value[2:6]
        try:
            code_point = int(hex_digits, 16)
            
            # Handle UTF-16 surrogate pairs - we need to look ahead for potential pairs
            if 0xD800 <= code_point <= 0xDBFF:  # High surrogate
                # Look ahead for potential low surrogate
                remaining_input = t.lexer.lexdata[t.lexer.lexpos:]
                import re
                low_surrogate_match = re.match(r'\\u[0-9a-fA-F]{4}', remaining_input)
                if low_surrogate_match:
                    low_hex = low_surrogate_match.group()[2:]
                    low_code_point = int(low_hex, 16)
                    if 0xDC00 <= low_code_point <= 0xDFFF:  # Valid low surrogate
                        # Combine high and low surrogate
                        combined_code_point = 0x10000 + ((code_point - 0xD800) << 10) + (low_code_point - 0xDC00)
                        unicode_char = chr(combined_code_point)
                        # Advance the lexer position past the low surrogate
                        t.lexer.lexpos += len(low_surrogate_match.group())
                    else:
                        # High surrogate followed by invalid low surrogate
                        raise JsonPathLexerError(f'Invalid surrogate sequence: high surrogate U+{code_point:04X} followed by non-low-surrogate U+{low_code_point:04X}')
                else:
                    # High surrogate not followed by unicode escape - invalid
                    raise JsonPathLexerError(f'Invalid surrogate sequence: unpaired high surrogate U+{code_point:04X}')
            elif 0xDC00 <= code_point <= 0xDFFF:  # Low surrogate without high surrogate
                raise JsonPathLexerError(f'Invalid surrogate sequence: unpaired low surrogate U+{code_point:04X}')
            else:
                # Regular BMP character
                unicode_char = chr(code_point)
            
            # Check if it's a control character that should be rejected
            if ord(unicode_char) <= 0x1F:
                raise JsonPathLexerError(f'Control character U+{ord(unicode_char):04X} is not allowed in string literals')
            t.lexer.string_value += unicode_char
        except ValueError:
            raise JsonPathLexerError(f'Invalid unicode escape sequence {t.value}')

    def t_doublequote_escape(self, t):
        r'\\.'
        escaped_char = t.value[1]
        escape_map = {
            '"': '"',
            '\\': '\\',
            '/': '/',
            'b': '\b',
            'f': '\f',
            'n': '\n',
            'r': '\r',
            't': '\t'
        }
        
        if escaped_char in escape_map:
            t.lexer.string_value += escape_map[escaped_char]
        else:
            raise JsonPathLexerError(f'Invalid escape sequence \\{escaped_char} in string literal')

    def t_doublequote_end(self, t):
        r'"'
        t.value = t.lexer.string_value
        t.type = 'STRING'  # Quoted strings are string literals
        t.lexer.string_value = None
        t.lexer.pop_state()
        return t

    def t_doublequote_error(self, t):
        raise JsonPathLexerError('Error on line %s, col %s while lexing doublequoted field: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))


    # Back-quoted "magic" operators
    t_backquote_ignore = ''
    def t_backquote(self, t):
        r'`'
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string_value = ''
        t.lexer.push_state('backquote')

    def t_backquote_escape(self, t):
        r'\\.'
        t.lexer.string_value += t.value[1]

    def t_backquote_content(self, t):
        r"[^`\\]+"
        t.lexer.string_value += t.value

    def t_backquote_end(self, t):
        r'`'
        t.value = t.lexer.string_value
        t.type = 'NAMED_OPERATOR'
        t.lexer.string_value = None
        t.lexer.pop_state()
        return t

    def t_backquote_error(self, t):
        raise JsonPathLexerError('Error on line %s, col %s while lexing backquoted operator: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))


    # Counting lines, handling errors
    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.latest_newline = t.lexpos

    def t_error(self, t):
        raise JsonPathLexerError('Error on line %s, col %s: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.lexer.latest_newline, t.value[0]))

if __name__ == '__main__':
    logging.basicConfig()
    lexer = JsonPathLexer(debug=True)
    for token in lexer.tokenize(sys.stdin.read()):
        print('%-20s%s' % (token.value, token.type))
