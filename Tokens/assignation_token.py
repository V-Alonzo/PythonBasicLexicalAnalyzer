from Tokens.token import Token

class AssignToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('ASSIGN', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid assignment operator."""
        return self.value == '='
    
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of an assignment token."""
        return char == '='
    
    def get_feedback(self):
        """Provides feedback on the token's validity."""
        if self.value != '=':
            return f"Invalid assignment operator. Expected '='."
