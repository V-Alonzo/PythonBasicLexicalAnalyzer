from Tokens.token import Token

class BOOLEAN(Token):
    BOOLEAN_VALUES : set[str] = {
        'true',
        'false'
    }
    

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('BOOLEAN', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid boolean."""
        if self.value in self.BOOLEAN_VALUES:
            self.type = self.value.upper()
            return True
        return False
    
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a boolean token."""
        return char.isalpha()
    
    def get_feedback(self):
        return f"Invalid boolean."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid boolean token with more characters."""
        return self.value == '' or any(boolean.startswith(self.value) for boolean in self.BOOLEAN_VALUES)