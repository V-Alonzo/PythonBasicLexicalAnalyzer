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


def classify_valid_lexeme(value):
    if value in KEYWORD_TYPES:
        return KEYWORD_TYPES[value]

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

    if value and value[0].isalpha() and value not in KEYWORD_TYPES:
        if all(char.isalnum() or char == "_" for char in value[1:]):
            return "IDENTIFIER"

    return None


def assert_expected_tokens_are_truthful(test_case, source_code, expected_tokens):
    cursor = 0

    for token_type, token_value, line, column in expected_tokens:
        while cursor < len(source_code) and source_code[cursor].isspace():
            cursor += 1

        if token_type == "EOF":
            test_case.assertEqual(token_value, "")
            test_case.assertEqual((line, column), index_to_line_column(source_code, len(source_code)))
            test_case.assertEqual(cursor, len(source_code))
            continue

        if token_type == "ERROR" and token_value == "EOF":
            test_case.assertEqual((line, column), index_to_line_column(source_code, len(source_code)))
            test_case.assertEqual(cursor, len(source_code))
            continue

        test_case.assertEqual((line, column), index_to_line_column(source_code, cursor))
        test_case.assertEqual(source_code[cursor:cursor + len(token_value)], token_value)

        if token_type == "ERROR":
            test_case.assertIsNone(classify_valid_lexeme(token_value))
        else:
            test_case.assertEqual(classify_valid_lexeme(token_value), token_type)

        cursor += len(token_value)


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
        "if_condition_with_delimiters",
        "if ( x < y && ! z ) { }",
        [
            ("IF", "if", 1, 1),
            ("LPAREN", "(", 1, 4),
            ("IDENTIFIER", "x", 1, 6),
            ("LESS_THAN", "<", 1, 8),
            ("IDENTIFIER", "y", 1, 10),
            ("AND", "&&", 1, 12),
            ("NOT", "!", 1, 15),
            ("IDENTIFIER", "z", 1, 17),
            ("RPAREN", ")", 1, 19),
            ("LBRACE", "{", 1, 21),
            ("RBRACE", "}", 1, 23),
            ("ERROR", "EOF", 1, 24),
            ("EOF", "", 1, 24),
        ],
    ),
    (
        "while_condition",
        "while ( counter <= 10 ) { }",
        [
            ("WHILE", "while", 1, 1),
            ("LPAREN", "(", 1, 7),
            ("IDENTIFIER", "counter", 1, 9),
            ("LESS_THAN_EQUAL", "<=", 1, 17),
            ("NUMBER", "10", 1, 20),
            ("RPAREN", ")", 1, 23),
            ("LBRACE", "{", 1, 25),
            ("RBRACE", "}", 1, 27),
            ("ERROR", "EOF", 1, 28),
            ("EOF", "", 1, 28),
        ],
    ),
    (
        "return_statement",
        "return value ;",
        [
            ("RETURN", "return", 1, 1),
            ("IDENTIFIER", "value", 1, 8),
            ("SEMICOLON", ";", 1, 14),
            ("EOF", "", 1, 15),
        ],
    ),
    (
        "identifier_with_underscore_and_digits",
        "variable_2 = 1 ;",
        [
            ("IDENTIFIER", "variable_2", 1, 1),
            ("ASSIGN", "=", 1, 12),
            ("NUMBER", "1", 1, 14),
            ("SEMICOLON", ";", 1, 16),
            ("EOF", "", 1, 17),
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
        "ifelse ",
        [
            ("IDENTIFIER", "ifelse", 1, 1),
            ("ERROR", "EOF", 1, 8),
            ("EOF", "", 1, 8),
        ],
    ),
    (
        "hexadecimal_number",
        "value = 0xFF ;",
        [
            ("IDENTIFIER", "value", 1, 1),
            ("ASSIGN", "=", 1, 7),
            ("HEX NUMBER", "0xFF", 1, 9),
            ("SEMICOLON", ";", 1, 14),
            ("EOF", "", 1, 15),
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
        "math_operators",
        "a + b - c * d / e ;",
        [
            ("IDENTIFIER", "a", 1, 1),
            ("PLUS", "+", 1, 3),
            ("IDENTIFIER", "b", 1, 5),
            ("MINUS", "-", 1, 7),
            ("IDENTIFIER", "c", 1, 9),
            ("MULTIPLY", "*", 1, 11),
            ("IDENTIFIER", "d", 1, 13),
            ("DIVIDE", "/", 1, 15),
            ("IDENTIFIER", "e", 1, 17),
            ("SEMICOLON", ";", 1, 19),
            ("EOF", "", 1, 20),
        ],
    ),
    (
        "extended_math_operators",
        "a % b ++ -- ;",
        [
            ("IDENTIFIER", "a", 1, 1),
            ("MODULO", "%", 1, 3),
            ("IDENTIFIER", "b", 1, 5),
            ("INCREMENT", "++", 1, 7),
            ("DECREMENT", "--", 1, 10),
            ("SEMICOLON", ";", 1, 13),
            ("EOF", "", 1, 14),
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
                ("NUMBER", "1", 1, 17),
                ("SEMICOLON", ";", 1, 19),
                ("EOF", "", 1, 20),
            ],
        )


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


class LexerIntegratedScenarioTests(unittest.TestCase):
    maxDiff = None

    def test_large_mixed_program_exercises_supported_features_together(self):
        source_code = '''int total = 0 ;
float average = 3.5 ;
if ( total <= 10 && ! done ) {
message = "hola ; mundo" ;
total = total + 1 - 2 * 3 / 4 ;
badId$ = 7 ;
badHex = 0xG1 ;
badNumber = 3.14d ;
check === != >= <= , return ;
} else {
while ( total != 0 ) {
total = total - 1 ;
}
logic = & ;
}
'''

        tokens = tokenize(source_code)

        expected_tokens = [
            ("INT", "int", 1, 1, None),
            ("IDENTIFIER", "total", 1, 5, None),
            ("ASSIGN", "=", 1, 11, None),
            ("NUMBER", "0", 1, 13, None),
            ("SEMICOLON", ";", 1, 15, None),
            ("FLOAT", "float", 2, 1, None),
            ("IDENTIFIER", "average", 2, 7, None),
            ("ASSIGN", "=", 2, 15, None),
            ("NUMBER", "3.5", 2, 17, None),
            ("SEMICOLON", ";", 2, 21, None),
            ("IF", "if", 3, 1, None),
            ("LPAREN", "(", 3, 4, None),
            ("IDENTIFIER", "total", 3, 6, None),
            ("LESS_THAN_EQUAL", "<=", 3, 12, None),
            ("NUMBER", "10", 3, 15, None),
            ("AND", "&&", 3, 18, None),
            ("NOT", "!", 3, 21, None),
            ("IDENTIFIER", "done", 3, 23, None),
            ("RPAREN", ")", 3, 28, None),
            ("LBRACE", "{", 3, 30, None),
            ("IDENTIFIER", "message", 4, 1, None),
            ("ASSIGN", "=", 4, 9, None),
            ("STRING", '"hola ; mundo"', 4, 11, None),
            ("SEMICOLON", ";", 4, 26, None),
            ("IDENTIFIER", "total", 5, 1, None),
            ("ASSIGN", "=", 5, 7, None),
            ("IDENTIFIER", "total", 5, 9, None),
            ("PLUS", "+", 5, 15, None),
            ("NUMBER", "1", 5, 17, None),
            ("MINUS", "-", 5, 19, None),
            ("NUMBER", "2", 5, 21, None),
            ("MULTIPLY", "*", 5, 23, None),
            ("NUMBER", "3", 5, 25, None),
            ("DIVIDE", "/", 5, 27, None),
            ("NUMBER", "4", 5, 29, None),
            ("SEMICOLON", ";", 5, 31, None),
            ("ERROR", "badId$", 6, 1, IDENTIFIER_FEEDBACK),
            ("ASSIGN", "=", 6, 8, None),
            ("NUMBER", "7", 6, 10, None),
            ("SEMICOLON", ";", 6, 12, None),
            ("IDENTIFIER", "badHex", 7, 1, None),
            ("ASSIGN", "=", 7, 8, None),
            ("ERROR", "0xG1", 7, 10, HEX_FEEDBACK),
            ("SEMICOLON", ";", 7, 15, None),
            ("IDENTIFIER", "badNumber", 8, 1, None),
            ("ASSIGN", "=", 8, 11, None),
            ("ERROR", "3.14d", 8, 13, NUMBER_FEEDBACK),
            ("SEMICOLON", ";", 8, 19, None),
            ("IDENTIFIER", "check", 9, 1, None),
            ("STRICT_EQUAL", "===", 9, 7, None),
            ("NOT_EQUAL", "!=", 9, 11, None),
            ("GREATER_THAN_EQUAL", ">=", 9, 14, None),
            ("LESS_THAN_EQUAL", "<=", 9, 17, None),
            ("COMMA", ",", 9, 20, None),
            ("RETURN", "return", 9, 22, None),
            ("SEMICOLON", ";", 9, 29, None),
            ("RBRACE", "}", 10, 1, None),
            ("ELSE", "else", 10, 3, None),
            ("LBRACE", "{", 10, 8, None),
            ("WHILE", "while", 11, 1, None),
            ("LPAREN", "(", 11, 7, None),
            ("IDENTIFIER", "total", 11, 9, None),
            ("NOT_EQUAL", "!=", 11, 15, None),
            ("NUMBER", "0", 11, 18, None),
            ("RPAREN", ")", 11, 20, None),
            ("LBRACE", "{", 11, 22, None),
            ("IDENTIFIER", "total", 12, 1, None),
            ("ASSIGN", "=", 12, 7, None),
            ("IDENTIFIER", "total", 12, 9, None),
            ("MINUS", "-", 12, 15, None),
            ("NUMBER", "1", 12, 17, None),
            ("SEMICOLON", ";", 12, 19, None),
            ("RBRACE", "}", 13, 1, None),
            ("IDENTIFIER", "logic", 14, 1, None),
            ("ASSIGN", "=", 14, 7, None),
            ("ERROR", "&", 14, 9, LOGICAL_FEEDBACK),
            ("SEMICOLON", ";", 14, 11, None),
            ("RBRACE", "}", 15, 1, None),
            ("ERROR", "EOF", 16, 1, EOF_FEEDBACK),
            ("EOF", "", 16, 1, None),
        ]

        assert_expected_tokens_are_truthful(
            self,
            source_code,
            [(token_type, token_value, line, column) for token_type, token_value, line, column, _ in expected_tokens],
        )

        self.assertEqual(
            [
                (token.type, token.value, token.line, token.column, getattr(token, "feedback", None))
                for token in tokens
            ],
            expected_tokens,
        )

        self.assertEqual(
            [token.value for token in tokens if isinstance(token, ErrorToken)],
            ["badId$", "0xG1", "3.14d", "&", "EOF"],
        )


def make_valid_test(source_code, expected_tokens):
    def test(self):
        self.assert_token_sequence(source_code, expected_tokens)

    return test


def make_error_test(source_code, expected_error, expected_eof):
    def test(self):
        self.assert_error_sequence(source_code, expected_error, expected_eof)

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


if __name__ == "__main__":
    unittest.main()
