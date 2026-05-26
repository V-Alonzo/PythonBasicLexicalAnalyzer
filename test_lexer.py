import unittest

from Lexer import Lexer
from Tokens.error_token import ErrorToken


KEYWORD_TYPES = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "return": "RETURN",
    "int": "INT",
    "float": "FLOAT",
    "double": "DOUBLE",
    "string": "STRING",
    "char": "CHAR",
    "bool": "BOOL",
}

BOOLEAN_LITERAL_TYPES = {
    "true": "TRUE",
    "false": "FALSE",
}

MATH_TYPES = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "%": "MODULO",
    "++": "INCREMENT",
    "--": "DECREMENT",
}

RELATIONAL_TYPES = {
    "<": "LESS_THAN",
    "<=": "LESS_THAN_EQUAL",
    ">": "GREATER_THAN",
    ">=": "GREATER_THAN_EQUAL",
    "==": "EQUAL",
    "===": "STRICT_EQUAL",
    "!=": "NOT_EQUAL",
}

LOGICAL_TYPES = {
    "&&": "AND",
    "||": "OR",
    "!": "NOT",
}

DELIMITER_TYPES = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
    ",": "COMMA",
}

IDENTIFIER_FEEDBACK = "Invalid identifier. Identifiers must start with a letter and can only contain letters, digits, and underscores. Additionally, identifiers cannot be keywords."
NUMBER_FEEDBACK = "Invalid number. Numbers can only contain digits and at most one decimal point."
HEX_FEEDBACK = "Invalid hexadecimal number. Hexadecimal numbers must start with '0x' followed by digits (0-9) and letters (A-F)."
LOGICAL_FEEDBACK = "Invalid logical operator."
RELATIONAL_FEEDBACK = "Invalid relational operator."
STRING_FEEDBACK = "Invalid string. Strings must start and end with double quotes."
MULTI_LINE_COMMENT_FEEDBACK = "Invalid multi-line comment. Comments must start with /* and end with */."
EOF_FEEDBACK = "Unexpected end of file."


def tokenize(source_code):
    return Lexer(source_code).tokenize()


def token_signature(token):
    return (token.type, token.value, token.line, token.column)


def token_details(token):
    return (token.type, token.value, token.line, token.column, getattr(token, "feedback", None))


def index_to_line_column(source_code, index):
    line = 1
    column = 1

    for char in source_code[:index]:
        if char == "\n":
            line += 1
            column = 1
        else:
            column += 1

    return (line, column)


def line_column_to_index(source_code, line, column):
    current_line = 1
    current_column = 1

    for index, char in enumerate(source_code):
        if (current_line, current_column) == (line, column):
            return index

        if char == "\n":
            current_line += 1
            current_column = 1
        else:
            current_column += 1

    if (current_line, current_column) == (line, column):
        return len(source_code)

    raise AssertionError(f"Position {(line, column)} does not exist in source code.")


def classify_valid_lexeme(value):
    if value in KEYWORD_TYPES:
        return KEYWORD_TYPES[value]

    if value in BOOLEAN_LITERAL_TYPES:
        return BOOLEAN_LITERAL_TYPES[value]

    if value in DELIMITER_TYPES:
        return DELIMITER_TYPES[value]

    if value.startswith("//"):
        return "SINGLE_LINE_COMMENT"

    if value.startswith("/*") and value.endswith("*/"):
        return "MULTI_LINE_COMMENT"

    if value in MATH_TYPES:
        return MATH_TYPES[value]

    if value in RELATIONAL_TYPES:
        return RELATIONAL_TYPES[value]

    if value in LOGICAL_TYPES:
        return LOGICAL_TYPES[value]

    if value == "=":
        return "ASSIGN"

    if value.startswith('"') and value.endswith('"'):
        return "STRING"

    if value.startswith("0x"):
        try:
            int(value, 16)
            return "HEX NUMBER"
        except ValueError:
            pass

    try:
        float(value)
        return "NUMBER"
    except ValueError:
        pass

    if value and value[0].isalpha() and value not in KEYWORD_TYPES and value not in BOOLEAN_LITERAL_TYPES:
        if all(char.isalnum() or char == "_" for char in value[1:]):
            return "IDENTIFIER"

    return None


def assert_expected_tokens_are_truthful(test_case, source_code, expected_tokens):
    previous_token = None

    for token_type, token_value, line, column in expected_tokens:
        if token_type == "EOF":
            test_case.assertEqual(token_value, "")
            test_case.assertEqual((line, column), index_to_line_column(source_code, len(source_code)))
            previous_token = (token_type, token_value, line, column)
            continue

        if token_type == "ERROR" and token_value == "EOF":
            test_case.assertEqual((line, column), index_to_line_column(source_code, len(source_code)))
            previous_token = (token_type, token_value, line, column)
            continue

        index = line_column_to_index(source_code, line, column)
        test_case.assertEqual(source_code[index:index + len(token_value)], token_value)

        if token_type != "ERROR":
            test_case.assertEqual(classify_valid_lexeme(token_value), token_type)
        else:
            is_semantic_overlay = (
                previous_token is not None
                and previous_token[1] == token_value
                and previous_token[2] == line
                and previous_token[3] == column
            )

            if not is_semantic_overlay:
                test_case.assertIsNone(classify_valid_lexeme(token_value))

        previous_token = (token_type, token_value, line, column)


VALID_CASES = [
    (
        "int_declaration",
        "int x = 42 ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "x", 1, 5),
            ("ASSIGN", "=", 1, 7),
            ("NUMBER", "42", 1, 9),
            ("SEMICOLON", ";", 1, 12),
            ("EOF", "", 1, 13),
        ],
    ),
    (
        "float_declaration",
        "float y = 3.14 ;",
        [
            ("FLOAT", "float", 1, 1),
            ("IDENTIFIER", "y", 1, 7),
            ("ASSIGN", "=", 1, 9),
            ("NUMBER", "3.14", 1, 11),
            ("SEMICOLON", ";", 1, 16),
            ("EOF", "", 1, 17),
        ],
    ),
    (
        "double_declaration",
        "double ratio = 3.14 ;",
        [
            ("DOUBLE", "double", 1, 1),
            ("IDENTIFIER", "ratio", 1, 8),
            ("ASSIGN", "=", 1, 14),
            ("NUMBER", "3.14", 1, 16),
            ("SEMICOLON", ";", 1, 21),
            ("EOF", "", 1, 22),
        ],
    ),
    (
        "string_declaration",
        'string name = "hi" ;',
        [
            ("STRING", "string", 1, 1),
            ("IDENTIFIER", "name", 1, 8),
            ("ASSIGN", "=", 1, 13),
            ("STRING", '"hi"', 1, 15),
            ("SEMICOLON", ";", 1, 20),
            ("EOF", "", 1, 21),
        ],
    ),
    (
        "bool_declaration_with_boolean_literal",
        "bool flag = true ;",
        [
            ("BOOL", "bool", 1, 1),
            ("IDENTIFIER", "flag", 1, 6),
            ("ASSIGN", "=", 1, 11),
            ("TRUE", "true", 1, 13),
            ("SEMICOLON", ";", 1, 18),
            ("EOF", "", 1, 19),
        ],
    ),
    (
        "if_condition_with_declared_identifiers",
        "int x = 1 ; int y = 2 ; bool z = false ; if ( x < y && ! z ) { }",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "x", 1, 5),
            ("ASSIGN", "=", 1, 7),
            ("NUMBER", "1", 1, 9),
            ("SEMICOLON", ";", 1, 11),
            ("INT", "int", 1, 13),
            ("IDENTIFIER", "y", 1, 17),
            ("ASSIGN", "=", 1, 19),
            ("NUMBER", "2", 1, 21),
            ("SEMICOLON", ";", 1, 23),
            ("BOOL", "bool", 1, 25),
            ("IDENTIFIER", "z", 1, 30),
            ("ASSIGN", "=", 1, 32),
            ("FALSE", "false", 1, 34),
            ("SEMICOLON", ";", 1, 40),
            ("IF", "if", 1, 42),
            ("LPAREN", "(", 1, 45),
            ("IDENTIFIER", "x", 1, 47),
            ("LESS_THAN", "<", 1, 49),
            ("IDENTIFIER", "y", 1, 51),
            ("AND", "&&", 1, 53),
            ("NOT", "!", 1, 56),
            ("IDENTIFIER", "z", 1, 58),
            ("RPAREN", ")", 1, 60),
            ("LBRACE", "{", 1, 62),
            ("RBRACE", "}", 1, 64),
            ("ERROR", "EOF", 1, 65),
            ("EOF", "", 1, 65),
        ],
    ),
    (
        "while_condition_with_declared_counter",
        "int counter = 0 ; while ( counter <= 10 ) { }",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "counter", 1, 5),
            ("ASSIGN", "=", 1, 13),
            ("NUMBER", "0", 1, 15),
            ("SEMICOLON", ";", 1, 17),
            ("WHILE", "while", 1, 19),
            ("LPAREN", "(", 1, 25),
            ("IDENTIFIER", "counter", 1, 27),
            ("LESS_THAN_EQUAL", "<=", 1, 35),
            ("NUMBER", "10", 1, 38),
            ("RPAREN", ")", 1, 41),
            ("LBRACE", "{", 1, 43),
            ("RBRACE", "}", 1, 45),
            ("ERROR", "EOF", 1, 46),
            ("EOF", "", 1, 46),
        ],
    ),
    (
        "return_statement_with_declared_identifier",
        "int value = 1 ; return value ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "value", 1, 5),
            ("ASSIGN", "=", 1, 11),
            ("NUMBER", "1", 1, 13),
            ("SEMICOLON", ";", 1, 15),
            ("RETURN", "return", 1, 17),
            ("IDENTIFIER", "value", 1, 24),
            ("SEMICOLON", ";", 1, 30),
            ("EOF", "", 1, 31),
        ],
    ),
    (
        "identifier_with_underscore_and_digits",
        "int variable_2 = 1 ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "variable_2", 1, 5),
            ("ASSIGN", "=", 1, 16),
            ("NUMBER", "1", 1, 18),
            ("SEMICOLON", ";", 1, 20),
            ("EOF", "", 1, 21),
        ],
    ),
    (
        "keyword_precedence_over_identifier",
        "if ",
        [
            ("IF", "if", 1, 1),
            ("ERROR", "EOF", 1, 4),
            ("EOF", "", 1, 4),
        ],
    ),
    (
        "identifier_similar_to_keyword",
        "int ifelse = 1 ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "ifelse", 1, 5),
            ("ASSIGN", "=", 1, 12),
            ("NUMBER", "1", 1, 14),
            ("SEMICOLON", ";", 1, 16),
            ("EOF", "", 1, 17),
        ],
    ),
    (
        "hexadecimal_number_assignment",
        "int value = 0xFF ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "value", 1, 5),
            ("ASSIGN", "=", 1, 11),
            ("HEX NUMBER", "0xFF", 1, 13),
            ("SEMICOLON", ";", 1, 18),
            ("EOF", "", 1, 19),
        ],
    ),
    (
        "string_with_spaces",
        '"hola mundo" ;',
        [
            ("STRING", '"hola mundo"', 1, 1),
            ("SEMICOLON", ";", 1, 14),
            ("EOF", "", 1, 15),
        ],
    ),
    (
        "string_with_delimiters_inside",
        '"x ; y { z }" ;',
        [
            ("STRING", '"x ; y { z }"', 1, 1),
            ("SEMICOLON", ";", 1, 15),
            ("EOF", "", 1, 16),
        ],
    ),
    (
        "math_operators_inside_assignment",
        "int result = 1 + 2 - 3 * 4 / 5 ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "result", 1, 5),
            ("ASSIGN", "=", 1, 12),
            ("NUMBER", "1", 1, 14),
            ("PLUS", "+", 1, 16),
            ("NUMBER", "2", 1, 18),
            ("MINUS", "-", 1, 20),
            ("NUMBER", "3", 1, 22),
            ("MULTIPLY", "*", 1, 24),
            ("NUMBER", "4", 1, 26),
            ("DIVIDE", "/", 1, 28),
            ("NUMBER", "5", 1, 30),
            ("SEMICOLON", ";", 1, 32),
            ("EOF", "", 1, 33),
        ],
    ),
    (
        "extended_math_operators_inside_assignment",
        "int result = 9 % 4 ++ -- ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "result", 1, 5),
            ("ASSIGN", "=", 1, 12),
            ("NUMBER", "9", 1, 14),
            ("MODULO", "%", 1, 16),
            ("NUMBER", "4", 1, 18),
            ("INCREMENT", "++", 1, 20),
            ("DECREMENT", "--", 1, 23),
            ("SEMICOLON", ";", 1, 26),
            ("EOF", "", 1, 27),
        ],
    ),
    (
        "relational_operators",
        "< <= > >= == === != ",
        [
            ("LESS_THAN", "<", 1, 1),
            ("LESS_THAN_EQUAL", "<=", 1, 3),
            ("GREATER_THAN", ">", 1, 6),
            ("GREATER_THAN_EQUAL", ">=", 1, 8),
            ("EQUAL", "==", 1, 11),
            ("STRICT_EQUAL", "===", 1, 14),
            ("NOT_EQUAL", "!=", 1, 18),
            ("ERROR", "EOF", 1, 21),
            ("EOF", "", 1, 21),
        ],
    ),
    (
        "logical_operators",
        "&& || ! ",
        [
            ("AND", "&&", 1, 1),
            ("OR", "||", 1, 4),
            ("NOT", "!", 1, 7),
            ("ERROR", "EOF", 1, 9),
            ("EOF", "", 1, 9),
        ],
    ),
    (
        "multi_line_comment_followed_by_code",
        "/* hola */ int x = 1 ;",
        [
            ("MULTI_LINE_COMMENT", "/* hola */", 1, 1),
            ("INT", "int", 1, 12),
            ("IDENTIFIER", "x", 1, 16),
            ("ASSIGN", "=", 1, 18),
            ("NUMBER", "1", 1, 20),
            ("SEMICOLON", ";", 1, 22),
            ("EOF", "", 1, 23),
        ],
    ),
    (
        "single_line_comment_without_final_semicolon",
        "// hola",
        [
            ("SINGLE_LINE_COMMENT", "// hola", 1, 1),
            ("ERROR", "EOF", 1, 8),
            ("EOF", "", 1, 8),
        ],
    ),
    (
        "multi_line_comment_without_final_semicolon",
        "/* hola */",
        [
            ("MULTI_LINE_COMMENT", "/* hola */", 1, 1),
            ("ERROR", "EOF", 1, 11),
            ("EOF", "", 1, 11),
        ],
    ),
    (
        "line_and_column_tracking_across_newline",
        "int x = 1 ;\nfloat y = 2 ;",
        [
            ("INT", "int", 1, 1),
            ("IDENTIFIER", "x", 1, 5),
            ("ASSIGN", "=", 1, 7),
            ("NUMBER", "1", 1, 9),
            ("SEMICOLON", ";", 1, 11),
            ("FLOAT", "float", 2, 1),
            ("IDENTIFIER", "y", 2, 7),
            ("ASSIGN", "=", 2, 9),
            ("NUMBER", "2", 2, 11),
            ("SEMICOLON", ";", 2, 13),
            ("EOF", "", 2, 14),
        ],
    ),
    (
        "trailing_whitespace_before_eof",
        "int ",
        [
            ("INT", "int", 1, 1),
            ("ERROR", "EOF", 1, 5),
            ("EOF", "", 1, 5),
        ],
    ),
]


ERROR_CASES = [
    (
        "invalid_identifier_symbol",
        "abc$ ",
        ("ERROR", "abc$", 1, 1, IDENTIFIER_FEEDBACK),
        ("EOF", "", 1, 6),
    ),
    (
        "invalid_number_suffix",
        "3.14d ",
        ("ERROR", "3.14d", 1, 1, NUMBER_FEEDBACK),
        ("EOF", "", 1, 7),
    ),
    (
        "invalid_hexadecimal_sequence",
        "0xG1 ",
        ("ERROR", "0xG1", 1, 1, HEX_FEEDBACK),
        ("EOF", "", 1, 6),
    ),
    (
        "single_ampersand_without_feedback",
        "& ",
        ("ERROR", "&", 1, 1, LOGICAL_FEEDBACK),
        ("EOF", "", 1, 3),
    ),
    (
        "double_exclamation_feedback",
        "!! ",
        ("ERROR", "!!", 1, 1, (LOGICAL_FEEDBACK, RELATIONAL_FEEDBACK)),
        ("EOF", "", 1, 4),
    ),
    (
        "unfinished_hexadecimal_prefix",
        "0x ",
        ("ERROR", "0x", 1, 1, HEX_FEEDBACK),
        ("EOF", "", 1, 4),
    ),
    (
        "unsupported_bracket_character",
        "[ ",
        ("ERROR", "[", 1, 1, ""),
        ("EOF", "", 1, 3),
    ),
    (
        "identifier_starting_with_digit",
        "1abc ",
        ("ERROR", "1abc", 1, 1, NUMBER_FEEDBACK),
        ("EOF", "", 1, 6),
    ),
    (
        "unterminated_string_reports_eof",
        '"hola',
        ("ERROR", '"hola', 1, 1, STRING_FEEDBACK),
        ("EOF", "", 1, 6),
    ),
    (
        "unterminated_multiline_comment_reports_eof",
        "/* hola",
        ("ERROR", "/* hola", 1, 1, MULTI_LINE_COMMENT_FEEDBACK),
        ("EOF", "", 1, 8),
    ),
]


SEMANTIC_CASES = [
    (
        "undeclared_assignment_reports_error_on_assign",
        "int x = 1 ; y = 2 ;",
        [
            ("INT", "int", 1, 1, None),
            ("IDENTIFIER", "x", 1, 5, None),
            ("ASSIGN", "=", 1, 7, None),
            ("NUMBER", "1", 1, 9, None),
            ("SEMICOLON", ";", 1, 11, None),
            ("IDENTIFIER", "y", 1, 13, None),
            ("ASSIGN", "=", 1, 15, None),
            ("ERROR", "=", 1, 15, "Undeclared variable: y"),
            ("NUMBER", "2", 1, 17, None),
            ("SEMICOLON", ";", 1, 19, None),
            ("EOF", "", 1, 20, None),
        ],
    ),
    (
        "scoped_variable_becomes_undeclared_after_block",
        "int x = 1 ; { int y = 2 ; y = 3 ; } y = 4 ;",
        [
            ("INT", "int", 1, 1, None),
            ("IDENTIFIER", "x", 1, 5, None),
            ("ASSIGN", "=", 1, 7, None),
            ("NUMBER", "1", 1, 9, None),
            ("SEMICOLON", ";", 1, 11, None),
            ("LBRACE", "{", 1, 13, None),
            ("INT", "int", 1, 15, None),
            ("IDENTIFIER", "y", 1, 19, None),
            ("ASSIGN", "=", 1, 21, None),
            ("NUMBER", "2", 1, 23, None),
            ("SEMICOLON", ";", 1, 25, None),
            ("IDENTIFIER", "y", 1, 27, None),
            ("ASSIGN", "=", 1, 29, None),
            ("NUMBER", "3", 1, 31, None),
            ("SEMICOLON", ";", 1, 33, None),
            ("RBRACE", "}", 1, 35, None),
            ("IDENTIFIER", "y", 1, 37, None),
            ("ASSIGN", "=", 1, 39, None),
            ("ERROR", "=", 1, 39, "Undeclared variable: y"),
            ("NUMBER", "4", 1, 41, None),
            ("SEMICOLON", ";", 1, 43, None),
            ("EOF", "", 1, 44, None),
        ],
    ),
    (
        "type_mismatch_reports_error_after_value",
        'int x = 1 ; x = "oops" ;',
        [
            ("INT", "int", 1, 1, None),
            ("IDENTIFIER", "x", 1, 5, None),
            ("ASSIGN", "=", 1, 7, None),
            ("NUMBER", "1", 1, 9, None),
            ("SEMICOLON", ";", 1, 11, None),
            ("IDENTIFIER", "x", 1, 13, None),
            ("ASSIGN", "=", 1, 15, None),
            ("STRING", '"oops"', 1, 17, None),
            ("ERROR", '"oops"', 1, 17, "Type mismatch: cannot assign value of type string to variable of type int"),
            ("SEMICOLON", ";", 1, 24, None),
            ("EOF", "", 1, 25, None),
        ],
    ),
    (
        "char_assignment_currently_reports_type_mismatch",
        'char c = "a" ;',
        [
            ("CHAR", "char", 1, 1, None),
            ("IDENTIFIER", "c", 1, 6, None),
            ("ASSIGN", "=", 1, 8, None),
            ("STRING", '"a"', 1, 10, None),
            ("ERROR", '"a"', 1, 10, "Type mismatch: cannot assign value of type string to variable of type char"),
            ("SEMICOLON", ";", 1, 14, None),
            ("EOF", "", 1, 15, None),
        ],
    ),
]


class LexerTokenizationTests(unittest.TestCase):
    maxDiff = None

    def assert_token_sequence(self, source_code, expected_tokens):
        assert_expected_tokens_are_truthful(self, source_code, expected_tokens)
        tokens = tokenize(source_code)
        self.assertEqual([token_signature(token) for token in tokens], expected_tokens)

    def test_single_line_comment_followed_by_code(self):
        tokens = tokenize("// hola\nint x = 1 ;")

        self.assertEqual(
            [token_signature(token) for token in tokens],
            [
                ("SINGLE_LINE_COMMENT", "// hola\nint", 1, 1),
                ("IDENTIFIER", "x", 1, 13),
                ("ASSIGN", "=", 1, 15),
                ("ERROR", "=", 1, 15),
                ("NUMBER", "1", 1, 17),
                ("SEMICOLON", ";", 1, 19),
                ("EOF", "", 1, 20),
            ],
        )
        self.assertEqual(tokens[3].feedback, "Undeclared variable: x")


class LexerErrorFeedbackTests(unittest.TestCase):
    maxDiff = None

    def assert_error_sequence(self, source_code, expected_error, expected_eof):
        expected_eof_error = ("ERROR", "EOF", expected_eof[2], expected_eof[3], EOF_FEEDBACK)

        assert_expected_tokens_are_truthful(self, source_code, [expected_error[:4], expected_eof_error[:4], expected_eof])
        tokens = tokenize(source_code)

        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], ErrorToken)
        self.assertEqual(token_signature(tokens[0]), expected_error[:4])
        expected_feedback = expected_error[4]

        if isinstance(expected_feedback, (tuple, list, set)):
            self.assertIn(tokens[0].feedback, expected_feedback)
        else:
            self.assertEqual(tokens[0].feedback, expected_feedback)

        self.assertIsInstance(tokens[1], ErrorToken)
        self.assertEqual(token_signature(tokens[1]), expected_eof_error[:4])
        self.assertEqual(tokens[1].feedback, expected_eof_error[4])
        self.assertEqual(token_signature(tokens[2]), expected_eof)

    def test_error_repr_hides_feedback_by_default(self):
        error_token = tokenize("abc$ ")[0]

        self.assertEqual(repr(error_token), "Token(ERROR, 'abc$', line=1, col=1)")

    def test_error_repr_shows_feedback_when_enabled(self):
        error_token = tokenize("abc$ ")[0]
        error_token.should_show_feedback = True

        self.assertEqual(
            repr(error_token),
            "Token(ERROR, 'abc$', line=1, col=1, feedback='Invalid identifier. Identifiers must start with a letter and can only contain letters, digits, and underscores. Additionally, identifiers cannot be keywords.')",
        )


class LexerSemanticAnalysisTests(unittest.TestCase):
    maxDiff = None

    def assert_token_details(self, source_code, expected_tokens):
        assert_expected_tokens_are_truthful(
            self,
            source_code,
            [(token_type, token_value, line, column) for token_type, token_value, line, column, _ in expected_tokens],
        )

        tokens = tokenize(source_code)
        self.assertEqual([token_details(token) for token in tokens], expected_tokens)


class LexerIntegratedScenarioTests(unittest.TestCase):
    maxDiff = None

    def test_large_mixed_program_exercises_scope_boolean_and_type_checks_together(self):
        source_code = '''int total = 0 ;
double average = 3.5 ;
bool done = false ;
string message = "hola" ;
if ( total <= 10 && ! done ) {
int inner = 1 ;
inner = 2 ;
}
inner = 3 ;
total = "oops" ;
'''

        tokens = tokenize(source_code)

        expected_tokens = [
            ("INT", "int", 1, 1, None),
            ("IDENTIFIER", "total", 1, 5, None),
            ("ASSIGN", "=", 1, 11, None),
            ("NUMBER", "0", 1, 13, None),
            ("SEMICOLON", ";", 1, 15, None),
            ("DOUBLE", "double", 2, 1, None),
            ("IDENTIFIER", "average", 2, 8, None),
            ("ASSIGN", "=", 2, 16, None),
            ("NUMBER", "3.5", 2, 18, None),
            ("SEMICOLON", ";", 2, 22, None),
            ("BOOL", "bool", 3, 1, None),
            ("IDENTIFIER", "done", 3, 6, None),
            ("ASSIGN", "=", 3, 11, None),
            ("FALSE", "false", 3, 13, None),
            ("SEMICOLON", ";", 3, 19, None),
            ("STRING", "string", 4, 1, None),
            ("IDENTIFIER", "message", 4, 8, None),
            ("ASSIGN", "=", 4, 16, None),
            ("STRING", '"hola"', 4, 18, None),
            ("SEMICOLON", ";", 4, 25, None),
            ("IF", "if", 5, 1, None),
            ("LPAREN", "(", 5, 4, None),
            ("IDENTIFIER", "total", 5, 6, None),
            ("LESS_THAN_EQUAL", "<=", 5, 12, None),
            ("NUMBER", "10", 5, 15, None),
            ("AND", "&&", 5, 18, None),
            ("NOT", "!", 5, 21, None),
            ("IDENTIFIER", "done", 5, 23, None),
            ("RPAREN", ")", 5, 28, None),
            ("LBRACE", "{", 5, 30, None),
            ("INT", "int", 6, 1, None),
            ("IDENTIFIER", "inner", 6, 5, None),
            ("ASSIGN", "=", 6, 11, None),
            ("NUMBER", "1", 6, 13, None),
            ("SEMICOLON", ";", 6, 15, None),
            ("IDENTIFIER", "inner", 7, 1, None),
            ("ASSIGN", "=", 7, 7, None),
            ("NUMBER", "2", 7, 9, None),
            ("SEMICOLON", ";", 7, 11, None),
            ("RBRACE", "}", 8, 1, None),
            ("IDENTIFIER", "inner", 9, 1, None),
            ("ASSIGN", "=", 9, 7, None),
            ("ERROR", "=", 9, 7, "Undeclared variable: inner"),
            ("NUMBER", "3", 9, 9, None),
            ("SEMICOLON", ";", 9, 11, None),
            ("IDENTIFIER", "total", 10, 1, None),
            ("ASSIGN", "=", 10, 7, None),
            ("STRING", '"oops"', 10, 9, None),
            ("ERROR", '"oops"', 10, 9, "Type mismatch: cannot assign value of type string to variable of type int"),
            ("SEMICOLON", ";", 10, 16, None),
            ("EOF", "", 11, 1, None),
        ]

        assert_expected_tokens_are_truthful(
            self,
            source_code,
            [(token_type, token_value, line, column) for token_type, token_value, line, column, _ in expected_tokens],
        )

        self.assertEqual([token_details(token) for token in tokens], expected_tokens)
        self.assertEqual(
            [token.feedback for token in tokens if isinstance(token, ErrorToken)],
            [
                "Undeclared variable: inner",
                "Type mismatch: cannot assign value of type string to variable of type int",
            ],
        )


def make_valid_test(source_code, expected_tokens):
    def test(self):
        self.assert_token_sequence(source_code, expected_tokens)

    return test


def make_error_test(source_code, expected_error, expected_eof):
    def test(self):
        self.assert_error_sequence(source_code, expected_error, expected_eof)

    return test


def make_semantic_test(source_code, expected_tokens):
    def test(self):
        self.assert_token_details(source_code, expected_tokens)

    return test


for case_name, source_code, expected_tokens in VALID_CASES:
    setattr(
        LexerTokenizationTests,
        f"test_{case_name}",
        make_valid_test(source_code, expected_tokens),
    )


for case_name, source_code, expected_error, expected_eof in ERROR_CASES:
    setattr(
        LexerErrorFeedbackTests,
        f"test_{case_name}",
        make_error_test(source_code, expected_error, expected_eof),
    )


for case_name, source_code, expected_tokens in SEMANTIC_CASES:
    setattr(
        LexerSemanticAnalysisTests,
        f"test_{case_name}",
        make_semantic_test(source_code, expected_tokens),
    )


if __name__ == "__main__":
    unittest.main()
