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
from SymbolTable import SymbolTable
from datatype_checker import check_type, type_exists, return_value_type
from Tokens.boolean_token import BOOLEAN

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.symbol_table = SymbolTable()
        self.assignable_tokens = [NumberToken, StringToken, BOOLEAN]

    def append_error_token(self, token_class: Token, feedback: str = ""):
        self.tokens.append(
            ErrorToken(
                token_class.line,
                token_class.column,
                self.tokens[-1] if self.tokens else None,
                token_class.value,
                feedback,
            )
        )

    def finalize_pending_token(self, tokens_classes: List[Token], error_token_class = None):
        best_token_type = self.determine_token_type(tokens_classes)

        if best_token_type is not None:
            best_token_type.previous_token = self.tokens[-1] if self.tokens else None
            self.tokens.append(best_token_type)

            if isinstance(best_token_type, IdentifierToken):
                if type_exists(best_token_type.previous_token.value):
                    # If the previous token is a type and the current token is an identifier, we are declaring a variable.
                    self.symbol_table.declare(best_token_type.value, best_token_type.previous_token.value)
                else:
                    # If the previous token is not a type, we are trying to use a variable.
                    # We need to check if the variable has been declared in any of the scopes.

                    if self.symbol_table.lookup(best_token_type.value) is None and self.peek_next_char() != "=":
                        #The variable does not exist in any scope, we have an error.
                        self.append_error_token(best_token_type, f"Undeclared variable: {best_token_type.value}")

            elif isinstance(best_token_type, AssignToken):
                # If the current token is an assignation operator, we need to check if the variable being assigned has been declared.
                variable_name = best_token_type.previous_token.value if best_token_type.previous_token else None
                variable_type = self.symbol_table.lookup(variable_name) if variable_name else None

                if variable_type is None:
                    # The variable being assigned has not been declared, we have an error.
                    self.append_error_token(best_token_type, f"Undeclared variable: {variable_name}")
                    return
                
            elif any([isinstance(best_token_type, token_type) for token_type in self.assignable_tokens]) and isinstance(best_token_type.previous_token, AssignToken):
                # If the current token is a value being assigned to a variable, we need to check if the type matches the variable one.
                variable_name = best_token_type.previous_token.previous_token.value if best_token_type.previous_token and best_token_type.previous_token.previous_token else None
                variable_type = self.symbol_table.lookup(variable_name) if variable_name else None

                if variable_type is not None and not check_type(best_token_type.value, variable_type):
                    # We have a type mismatch error.
                    self.append_error_token(best_token_type, f"Type mismatch: cannot assign value of type {return_value_type(best_token_type.value)} to variable of type {variable_type}")
                elif variable_type is None:
                    # The variable being assigned has not been declared, we have an error.
                    self.append_error_token(best_token_type, f"Undeclared variable: {variable_name}")
                    return

            
        elif error_token_class is not None and not error_token_class.value.isspace() and error_token_class.value != "":
            self.append_error_token(error_token_class, error_token_class.get_feedback())
            return

        elif tokens_classes[0].value != "" and not tokens_classes[0].value.isspace():
            self.append_error_token(tokens_classes[0])


    def finalize_eof(self, tokens_classes: List[Token], error_token_class = None):
        self.finalize_pending_token(tokens_classes, error_token_class)

        if len(self.tokens) == 0 or self.tokens[-1].value != ";":
            self.tokens.append(ErrorToken(self.line, self.column, self.tokens[-1] if self.tokens else None, "EOF", "Unexpected end of file."))

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
            if all(isinstance(valid_class, BOOLEAN) or isinstance(valid_class, IdentifierToken) for valid_class in valid_classes):
                return valid_classes[0] if isinstance(valid_classes[0], BOOLEAN) else valid_classes[1]
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
            SingleLineCommentToken(line, column, previous_token),
            BOOLEAN(line, column, previous_token)
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
                    if currCharacter == "{":
                        self.symbol_table.enter_scoppe()
                        print(self.symbol_table.scopes)
                    elif currCharacter == "}":
                        self.symbol_table.exit_scope()
                        print(self.symbol_table.scopes)
                    
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
    source_code = '''

int x = 10;

{

    int y = 20;

    y = 50;

}

y = 50;

x = 20;

x < z;
    
    '''

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