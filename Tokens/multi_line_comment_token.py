from Tokens.token import Token

class MultiLineCommentToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('MULTI_LINE_COMMENT', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid multi-line comment."""
        return self.value.startswith('/*') and self.value.endswith('*/')

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a multi-line comment."""
        return isinstance(char, str)
    
    def get_feedback(self):
        return f"Invalid multi-line comment. Comments must start with /* and end with */."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid multi-line comment token with more characters."""
        return self.value == '' or (self.value.startswith('/*') and not self.value.endswith('*/')) or (self.value.startswith('/*') and self.value.endswith('*/'))