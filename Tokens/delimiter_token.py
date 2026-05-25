from Tokens.token import Token

class DelimiterToken(Token):

    delimiters = {
        "(":"LPAREN",
        ")":"RPAREN",
        "{":"LBRACE",
        "}":"RBRACE",
        ";":"SEMICOLON",
        ",":"COMMA"
    }

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('DELIMITER', value, line, column, previous_token)
        self.verify_current_state()

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid delimiter."""
        if self.value in self.delimiters:
            self.type = self.delimiters[self.value]
            return True
        
        return False
    
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a delimiter token."""
        return char in self.delimiters
    
    def get_feedback(self):
        return "Invalid delimiter."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid delimiter token with more characters."""
        return self.value == '' or any(delimiter.startswith(self.value) for delimiter in self.delimiters)
