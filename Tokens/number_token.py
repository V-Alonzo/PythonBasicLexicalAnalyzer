from Tokens.token import Token

class NumberToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('NUMBER', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid number."""
        try:
            float(self.value)
            return True
        except ValueError:
            return False

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a number token."""
        return char.isdigit() or char == '.'
    
    def get_feedback(self):
        return f"Invalid number. Numbers can only contain digits and at most one decimal point."