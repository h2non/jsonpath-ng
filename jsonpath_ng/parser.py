import logging
import sys
import os.path

import ply.yacc

from jsonpath_ng.exceptions import JsonPathParserError
from jsonpath_ng.jsonpath import *
from jsonpath_ng.lexer import JsonPathLexer

logger = logging.getLogger(__name__)


def parse(string):
    return JsonPathParser().parse(string)


class JsonPathParser:
    '''
    An LALR-parser for JsonPath
    '''

    tokens = JsonPathLexer.tokens

    def __init__(self, debug=False, lexer_class=None):
        if self.__doc__ is None:
            raise JsonPathParserError(
                'Docstrings have been removed! By design of PLY, '
                'jsonpath-rw requires docstrings. You must not use '
                'PYTHONOPTIMIZE=2 or python -OO.'
            )

        self.debug = debug
        self.lexer_class = lexer_class or JsonPathLexer # Crufty but works around statefulness in PLY

        # Since PLY has some crufty aspects and dumps files, we try to keep them local
        # However, we need to derive the name of the output Python file :-/
        output_directory = os.path.dirname(__file__)
        try:
            module_name = os.path.splitext(os.path.split(__file__)[1])[0]
        except:
            module_name = __name__

        start_symbol = 'jsonpath'
        parsing_table_module = '_'.join([module_name, start_symbol, 'parsetab'])

        # Generate the parse table
        self.parser = ply.yacc.yacc(module=self,
                                    debug=self.debug,
                                    tabmodule = parsing_table_module,
                                    outputdir = output_directory,
                                    write_tables=0,
                                    start = start_symbol,
                                    errorlog = logger)

    def parse(self, string, lexer = None) -> JSONPath:
        # Validate no leading or trailing whitespace per RFC 9535
        if string != string.strip():
            raise JsonPathParserError('JSONPath expressions must not have leading or trailing whitespace')
        
        lexer = lexer or self.lexer_class()
        return self.parse_token_stream(lexer.tokenize(string))

    def parse_token_stream(self, token_iterator):
        return self.parser.parse(lexer = IteratorToTokenStream(token_iterator))

    # ===================== PLY Parser specification =====================

    precedence = [
        ('left', ','),
        ('left', 'DOUBLEDOT'),
        ('left', '.'),
        ('left', '[', ']'),  # Higher precedence for brackets
        ('left', '|'),
        ('left', '&'),
        ('left', 'WHERE'),
        ('left', 'WHERENOT'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
        ('right', '!'),  # Right associative for unary NOT
    ]

    def p_error(self, t):
        if t is None:
            raise JsonPathParserError('Parse error near the end of string!')
        raise JsonPathParserError('Parse error at %s:%s near token %s (%s)'
                                  % (t.lineno, t.col, t.value, t.type))

    def p_jsonpath_binop(self, p):
        """jsonpath : jsonpath '.' jsonpath
                    | jsonpath DOUBLEDOT jsonpath
                    | jsonpath WHERE jsonpath
                    | jsonpath WHERENOT jsonpath
                    | jsonpath '|' jsonpath
                    | jsonpath '&' jsonpath"""
        op = p[2]

        if op == '.':
            p[0] = Child(p[1], p[3])
        elif op == '..':
            p[0] = Descendants(p[1], p[3])
        elif op == 'where':
            p[0] = Where(p[1], p[3])
        elif op == 'wherenot':
            p[0] = WhereNot(p[1], p[3])
        elif op == '|':
            p[0] = Union(p[1], p[3])
        elif op == '&':
            p[0] = Intersect(p[1], p[3])

    def p_jsonpath_fields(self, p):
        "jsonpath : fields_or_any"
        if isinstance(p[1], str):
            p[0] = Fields(p[1])
        else:
            p[0] = Fields(*p[1])

    def p_jsonpath_named_operator(self, p):
        "jsonpath : NAMED_OPERATOR"
        if p[1] == 'this':
            p[0] = This()
        elif p[1] == 'parent':
            p[0] = Parent()
        else:
            raise JsonPathParserError('Unknown named operator `%s` at %s:%s'
                                      % (p[1], p.lineno(1), p.lexpos(1)))

    def p_jsonpath_root(self, p):
        "jsonpath : '$'"
        p[0] = Root()

    def p_jsonpath_current(self, p):
        "jsonpath : CURRENT"
        p[0] = CurrentNode()


    def p_empty(self, p):
        'empty :'
        pass
    

    def p_jsonpath_bracket_field(self, p):
        """jsonpath : '[' ID ']'"""
        p[0] = Fields(p[2])

    def p_jsonpath_bracket_string(self, p):
        """jsonpath : '[' STRING ']'"""
        p[0] = Fields(p[2])

    def p_jsonpath_bracket_index(self, p):
        """jsonpath : '[' NUMBER ']'"""
        # Validate index constraints per JSONPath RFC
        index = p[2]
        if not isinstance(index, int):
            raise JsonPathParserError(f'Array indices must be integers, not {type(index).__name__}: {index}')
        # Check for negative zero which is invalid as an array index
        # PLY gives us the token object as p.slice[2], check if it has original_str
        if hasattr(p.slice[2], 'original_str') and p.slice[2].original_str == '-0':
            raise JsonPathParserError('Negative zero (-0) is not allowed as an array index')
        # Check for indices beyond safe integer range (2^53 - 1)
        if abs(index) > 9007199254740991:
            raise JsonPathParserError(f'Array index {index} exceeds maximum safe integer range')
        p[0] = Index(p[2])

    def p_jsonpath_bracket_wildcard(self, p):
        """jsonpath : '[' '*' ']'"""
        p[0] = Fields('*')

    def p_jsonpath_bracket_slice(self, p):
        """jsonpath : '[' slice ']'"""
        p[0] = p[2]

    def p_jsonpath_bracket_union(self, p):
        """jsonpath : '[' union_list ']'"""
        if len(p[2]) == 1:
            p[0] = p[2][0]
        else:
            result = p[2][0]
            for element in p[2][1:]:
                result = Union(result, element)
            p[0] = result

    def p_jsonpath_child_bracket_field(self, p):
        """jsonpath : jsonpath '[' ID ']'"""
        p[0] = Child(p[1], Fields(p[3]))

    def p_jsonpath_child_bracket_string(self, p):
        """jsonpath : jsonpath '[' STRING ']'"""
        p[0] = Child(p[1], Fields(p[3]))

    def p_jsonpath_child_bracket_index(self, p):
        """jsonpath : jsonpath '[' NUMBER ']'"""
        # Validate index constraints per JSONPath RFC
        index = p[3]
        if not isinstance(index, int):
            raise JsonPathParserError(f'Array indices must be integers, not {type(index).__name__}: {index}')
        # Check for negative zero which is invalid as an array index
        if hasattr(p.slice[3], 'original_str') and p.slice[3].original_str == '-0':
            raise JsonPathParserError('Negative zero (-0) is not allowed as an array index')
        # Check for indices beyond safe integer range (2^53 - 1)
        if abs(index) > 9007199254740991:
            raise JsonPathParserError(f'Array index {index} exceeds maximum safe integer range')
        p[0] = Child(p[1], Index(p[3]))

    def p_jsonpath_child_bracket_wildcard(self, p):
        """jsonpath : jsonpath '[' '*' ']'"""
        p[0] = Child(p[1], Fields('*'))

    def p_jsonpath_child_bracket_slice(self, p):
        """jsonpath : jsonpath '[' slice ']'"""
        p[0] = Child(p[1], p[3])

    def p_jsonpath_child_bracket_union(self, p):
        """jsonpath : jsonpath '[' union_list ']'"""
        if len(p[3]) == 1:
            p[0] = Child(p[1], p[3][0])
        else:
            result = p[3][0]
            for element in p[3][1:]:
                result = Union(result, element)
            p[0] = Child(p[1], result)

    def p_union_list_start(self, p):
        """union_list : union_element ',' union_element"""
        p[0] = [p[1], p[3]]

    def p_union_list_extend(self, p):
        """union_list : union_list ',' union_element"""
        p[0] = p[1] + [p[3]]

    def p_union_element_field(self, p):
        """union_element : ID"""
        p[0] = Fields(p[1])

    def p_union_element_string(self, p):
        """union_element : STRING"""
        p[0] = Fields(p[1])

    def p_union_element_index(self, p):
        """union_element : NUMBER"""
        # Validate index constraints per JSONPath RFC
        index = p[1]
        if not isinstance(index, int):
            raise JsonPathParserError(f'Array indices must be integers, not {type(index).__name__}: {index}')
        # Check for negative zero which is invalid as an array index
        if hasattr(p.slice[1], 'original_str') and p.slice[1].original_str == '-0':
            raise JsonPathParserError('Negative zero (-0) is not allowed as an array index')
        # Check for indices beyond safe integer range (2^53 - 1)
        if abs(index) > 9007199254740991:
            raise JsonPathParserError(f'Array index {index} exceeds maximum safe integer range')
        p[0] = Index(p[1])

    def p_union_element_wildcard(self, p):
        """union_element : '*'"""
        p[0] = Fields('*')

    def p_union_element_slice(self, p):
        """union_element : slice"""
        p[0] = p[1]

    def p_union_element_filter(self, p):
        """union_element : '?' filter_expr"""
        p[0] = Filter(p[2])

    def p_jsonpath_parens(self, p):
        "jsonpath : '(' jsonpath ')'"
        p[0] = p[2]

    # Field parsing for dot notation - only identifiers and wildcards allowed
    def p_fields_or_any(self, p):
        """fields_or_any : fields
                         | '*'"""
        if p[1] == '*':
            p[0] = ['*']
        else:
            p[0] = p[1]

    def p_fields_id(self, p):
        "fields : ID"
        p[0] = [p[1]]

    # Temporarily disabled to prevent conflict with function call arguments
    # TODO: Fix grammar to allow both function calls and comma-separated fields
    # def p_fields_comma(self, p):
    #     "fields : fields ',' fields"
    #     p[0] = p[1] + p[3]

    def p_slice_any(self, p):
        "slice : '*'"
        p[0] = Slice()

    def p_slice(self, p): # Currently does not support `step`
        """slice : maybe_int ':' maybe_int
                 | maybe_int ':' maybe_int ':' maybe_int """
        p[0] = Slice(*p[1::2])

    def p_maybe_int(self, p):
        """maybe_int : NUMBER
                     | empty"""
        p[0] = p[1]


    # Filter expression rules
    def p_jsonpath_filter(self, p):
        "jsonpath : '[' '?' filter_expr ']'"
        p[0] = Filter(p[3])

    def p_jsonpath_child_filter(self, p):
        "jsonpath : jsonpath '[' '?' filter_expr ']'"
        p[0] = Child(p[1], Filter(p[4]))

    def p_filter_expr_comparison(self, p):
        """filter_expr : filter_expr EQ filter_expr
                       | filter_expr NE filter_expr
                       | filter_expr LT filter_expr
                       | filter_expr LE filter_expr
                       | filter_expr GT filter_expr
                       | filter_expr GE filter_expr"""
        p[0] = Comparison(p[1], p[2], p[3])

    def p_filter_expr_logical(self, p):
        """filter_expr : filter_expr AND filter_expr
                       | filter_expr OR filter_expr"""
        if p[2] == '&&':
            p[0] = LogicalAnd(p[1], p[3])
        else:
            p[0] = LogicalOr(p[1], p[3])

    def p_filter_expr_not(self, p):
        """filter_expr : '!' filter_expr"""
        p[0] = LogicalNot(p[2])

    def p_filter_expr_current(self, p):
        "filter_expr : CURRENT"
        p[0] = CurrentNode()

    def p_filter_expr_path(self, p):
        "filter_expr : jsonpath"
        p[0] = p[1]

    def p_filter_expr_literal_number(self, p):
        "filter_expr : NUMBER"
        p[0] = Literal(p[1])

    def p_filter_expr_literal_null(self, p):
        "filter_expr : NULL"
        p[0] = Literal(None)

    def p_filter_expr_literal_true(self, p):
        "filter_expr : TRUE"
        p[0] = Literal(True)

    def p_filter_expr_literal_false(self, p):
        "filter_expr : FALSE"
        p[0] = Literal(False)

    def p_filter_expr_field(self, p):
        "filter_expr : ID"
        p[0] = Fields(p[1])

    def p_filter_expr_string(self, p):
        "filter_expr : STRING"
        p[0] = Literal(p[1])

    def p_filter_expr_parens(self, p):
        "filter_expr : '(' filter_expr ')'"
        p[0] = p[2]
    
    def p_filter_expr_function_call_two_args(self, p):
        "filter_expr : ID '(' filter_expr ',' filter_expr ')'"
        p[0] = FunctionCall(p[1], [p[3], p[5]])
    
    def p_filter_expr_function_call_single(self, p):
        "filter_expr : ID '(' filter_expr ')'"
        p[0] = FunctionCall(p[1], [p[3]])
    

class IteratorToTokenStream:
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None


if __name__ == '__main__':
    logging.basicConfig()
    parser = JsonPathParser(debug=True)
    print(parser.parse(sys.stdin.read()))
