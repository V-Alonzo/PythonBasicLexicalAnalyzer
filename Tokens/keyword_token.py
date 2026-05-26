from Tokens.token import Token

class KEYWORD(Token):
    KEYWORDS : set[str] = {
        'if',
        'else',
        'while',
        'return',
        'int',
        'float',
        'double',
        'string',
        'char',
        'bool'
    }

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('KEYWORD', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid keyword."""
        if self.value in self.KEYWORDS:
            self.type = self.value.upper()
            return True
        return False
    
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a keyword token."""
        return char.isalpha()
    
    def get_feedback(self):
        return f"Invalid keyword."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid keyword token with more characters."""
        return self.value == '' or any(keyword.startswith(self.value) for keyword in self.KEYWORDS)