from Tokens.token import Token
from typing import List, Optional
from Tokens.keyword_token import KEYWORD
from Tokens.delimiter_token import DelimiterToken
from Tokens.math_token import MathToken
from Tokens.identifier_token import IdentifierToken
from Tokens.number_token import NumberToken
from Tokens.error_token import ErrorToken
from Tokens.relational_token import RelationalToken
from Tokens.assignation_token import AssignToken
from Tokens.EOF_token import EOFToken
from Tokens.logical_token import LogicalToken
from Tokens.hexadecimal_number_token import HexNumberToken
from Tokens.string_token import StringToken
from Tokens.multi_line_comment_token import MultiLineCommentToken
from Tokens.single_line_token import SingleLineCommentToken

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def append_error_token(self, token_class: Token, feedback: str = ""):
        self.tokens.append(
            ErrorToken(
                token_class.line,
                token_class.column,
                None,
                token_class.value,
                feedback,
            )
        )

    def finalize_pending_token(self, tokens_classes: List[Token], error_token_class = None):
        best_token_type = self.determine_token_type(tokens_classes)

        if best_token_type is not None:
            self.tokens.append(best_token_type)
            return

        if error_token_class is not None and not error_token_class.value.isspace() and error_token_class.value != "":
            self.append_error_token(error_token_class, error_token_class.get_feedback())
            return

        if tokens_classes[0].value != "" and not tokens_classes[0].value.isspace():
            self.append_error_token(tokens_classes[0])

    def finalize_eof(self, tokens_classes: List[Token], error_token_class = None):
        self.finalize_pending_token(tokens_classes, error_token_class)

        if len(self.tokens) == 0 or self.tokens[-1].type != "SEMICOLON":
            self.tokens.append(ErrorToken(self.line, self.column, None, "EOF", "Unexpected end of file."))

        self.tokens.append(EOFToken(self.line, self.column, self.tokens[-1] if self.tokens else None))
        return self.tokens

    def get_next_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        
        char = self.source[self.position]
        self.position += 1
        
        return char
    
    def determine_token_type(self, tokens_classes: List[Token]) -> Optional[Token]:
        valid_classes = []
        for token_class in tokens_classes:
            if token_class.check_validity_token():
                valid_classes.append(token_class)

        if len(valid_classes) == 1:
            return valid_classes[0]
        
        elif len(valid_classes) > 1:
            if any(isinstance(valid_class, StringToken) for valid_class in valid_classes):
                return list(filter(lambda valid_class: isinstance(valid_class, StringToken), valid_classes))[0] 
            if all(isinstance(valid_class, KEYWORD) or isinstance(valid_class, IdentifierToken) for valid_class in valid_classes):
                return valid_classes[0] if isinstance(valid_classes[0], KEYWORD) else valid_classes[1]
        else:
            return None
        

    def peek_next_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
        

    def generate_token_classes(self, line, column, previous_token = None) -> List[Token]:
        return [
            KEYWORD(line, column, previous_token),
            MathToken(line, column, previous_token),
            IdentifierToken(line, column, previous_token),
            NumberToken(line, column, previous_token),
            RelationalToken(line, column, previous_token),
            AssignToken(line, column, previous_token),
            LogicalToken(line, column, previous_token),
            HexNumberToken(line, column, previous_token),
            StringToken(line, column, previous_token),
            MultiLineCommentToken(line, column, previous_token),
            SingleLineCommentToken(line, column, previous_token)
        ]


    def tokenize(self) -> List[Token]:
        
        tokens_classes = self.generate_token_classes(self.line, self.column)

        delimiter_helper = DelimiterToken(self.line, self.column)

        currCharacter = self.get_next_char()

        is_building_string = False
        is_building_comment = False
        is_building_single_line_comment = False

        error_token_class = None

        while currCharacter is not None:

            while currCharacter is not None and not is_building_string and not is_building_comment and not is_building_single_line_comment and (currCharacter.isspace() or currCharacter in ['\n'] or delimiter_helper.is_valid_char(currCharacter)):
                self.finalize_pending_token(tokens_classes, error_token_class)

                error_token_class = None

                if delimiter_helper.is_valid_char(currCharacter):
                    self.tokens.append(DelimiterToken(self.line, self.column, self.tokens[-1] if self.tokens else None, currCharacter))

                self.line += 1 if currCharacter == '\n' else 0
                self.column = 1 if currCharacter == '\n' else self.column + 1

                currCharacter = self.get_next_char()
                tokens_classes = self.generate_token_classes(self.line, self.column, self.tokens[-1] if self.tokens else None)

                if currCharacter is None:
                    return self.finalize_eof(tokens_classes)

            if currCharacter == '"':
                is_building_string = not is_building_string
            elif currCharacter == '/' and self.peek_next_char() == '*':
                is_building_comment = True
            elif currCharacter == '*' and self.peek_next_char() == '/':
                is_building_comment = False
            elif currCharacter == '/' and self.peek_next_char() == '/':
                is_building_single_line_comment = True
            elif currCharacter == '\n' and is_building_single_line_comment:
                is_building_single_line_comment = False

            for token_class in tokens_classes:
                token_class.append_char(currCharacter)


            still_valid_token_classes = [possible_valid_class for possible_valid_class in tokens_classes if possible_valid_class.could_be_valid_token()]
            if len(still_valid_token_classes) == 1:
                error_token_class = still_valid_token_classes[0]


            currCharacter = self.get_next_char()
            self.column += 1

        return self.finalize_eof(tokens_classes, error_token_class)

if __name__ == "__main__":
    #Source code must always have a space between tokens, 
    #otherwise the lexer will not be able to determine the correct token type. 
    #For example, 
    #"intx=42;" must be written as "int x = 42;" to be correctly tokenized.
    source_code = '''// hola\nint x = 1 ;'''

    my_lexer = Lexer(source_code)

    final_tokens = my_lexer.tokenize()

    print("=" * 60)
    print("SOURCE CODE")
    print(source_code)
    print("=" * 60)
    print("\nLEXICAL ANALYSIS:")
    print("-" * 60)

    for token in final_tokens:
        print(token)

    print("=" * 60)
    print("ERROR FEEDBACK:")
    print("-" * 60)

    for token in final_tokens:
        if isinstance(token, ErrorToken):
            token.should_show_feedback = True
            print(token)
            print("-"*60)