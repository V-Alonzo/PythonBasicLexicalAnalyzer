from Tokens.token import Token

class StringToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('STRING', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid string."""
        return self.value.startswith('"') and self.value.endswith('"')

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a string."""
        return isinstance(char, str)
    
    def get_feedback(self):
        return f"Invalid string. Strings must start and end with double quotes."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid string token with more characters."""
        return self.value == '' or (self.value.startswith('"') and not self.value.endswith('"')) or (self.value.startswith('"') and self.value.endswith('"'))