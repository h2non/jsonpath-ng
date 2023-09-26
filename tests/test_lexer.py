import logging
import unittest

from ply.lex import LexToken

from jsonpath_ng.lexer import JsonPathLexer, JsonPathLexerError

class TestLexer(unittest.TestCase):

    def token(self, value, ty=None):
        t = LexToken()
        t.type = ty if ty != None else value
        t.value = value
        t.lineno = -1
        t.lexpos = -1
        return t

    def assert_lex_equiv(self, s, stream2):
        # NOTE: lexer fails to reset after call?
        l = JsonPathLexer(debug=True)
        stream1 = list(l.tokenize(s)) # Save the stream for debug output when a test fails
        stream2 = list(stream2)
        assert len(stream1) == len(stream2)
        for token1, token2 in zip(stream1, stream2):
            print(token1, token2)
            assert token1.type  == token2.type
            assert token1.value == token2.value

    @classmethod
    def setup_class(cls):
        logging.basicConfig()

    def test_simple_inputs(self):
        self.assert_lex_equiv('$', [self.token('$', '$')])
        self.assert_lex_equiv('"hello"', [self.token('hello', 'ID')])
        self.assert_lex_equiv("'goodbye'", [self.token('goodbye', 'ID')])
        self.assert_lex_equiv("'doublequote\"'", [self.token('doublequote"', 'ID')])
        self.assert_lex_equiv(r'"doublequote\""', [self.token('doublequote"', 'ID')])
        self.assert_lex_equiv(r"'singlequote\''", [self.token("singlequote'", 'ID')])
        self.assert_lex_equiv('"singlequote\'"', [self.token("singlequote'", 'ID')])
        self.assert_lex_equiv('fuzz', [self.token('fuzz', 'ID')])
        self.assert_lex_equiv('1', [self.token(1, 'NUMBER')])
        self.assert_lex_equiv('45', [self.token(45, 'NUMBER')])
        self.assert_lex_equiv('-1', [self.token(-1, 'NUMBER')])
        self.assert_lex_equiv(' -13 ', [self.token(-13, 'NUMBER')])
        self.assert_lex_equiv('"fuzz.bang"', [self.token('fuzz.bang', 'ID')])
        self.assert_lex_equiv('fuzz.bang', [self.token('fuzz', 'ID'), self.token('.', '.'), self.token('bang', 'ID')])
        self.assert_lex_equiv('fuzz.*', [self.token('fuzz', 'ID'), self.token('.', '.'), self.token('*', '*')])
        self.assert_lex_equiv('fuzz..bang', [self.token('fuzz', 'ID'), self.token('..', 'DOUBLEDOT'), self.token('bang', 'ID')])
        self.assert_lex_equiv('&', [self.token('&', '&')])
        self.assert_lex_equiv('@', [self.token('@', 'ID')])
        self.assert_lex_equiv('`this`', [self.token('this', 'NAMED_OPERATOR')])
        self.assert_lex_equiv('|', [self.token('|', '|')])
        self.assert_lex_equiv('where', [self.token('where', 'WHERE')])

    def test_basic_errors(self):
        def tokenize(s):
            l = JsonPathLexer(debug=True)
            return list(l.tokenize(s))

        self.assertRaises(JsonPathLexerError, tokenize, "'\"")
        self.assertRaises(JsonPathLexerError, tokenize, '"\'')
        self.assertRaises(JsonPathLexerError, tokenize, '`"')
        self.assertRaises(JsonPathLexerError, tokenize, "`'")
        self.assertRaises(JsonPathLexerError, tokenize, '"`')
        self.assertRaises(JsonPathLexerError, tokenize, "'`")
        self.assertRaises(JsonPathLexerError, tokenize, '?')
        self.assertRaises(JsonPathLexerError, tokenize, '$.foo.bar.#')
