from Tokens.token import Token

class SingleLineCommentToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('SINGLE_LINE_COMMENT', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid single-line comment."""
        return self.value.startswith('//')

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a single-line comment."""
        return isinstance(char, str)
    
    def get_feedback(self):
        return f"Invalid single-line comment. Comments must start with //."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid single-line comment token with more characters."""
        return self.value == '' or (self.value.startswith('//') and not self.value.endswith('\n')) or (self.value.startswith('//') and self.value.endswith('\n'))