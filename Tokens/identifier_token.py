from Tokens.token import Token
from Tokens.keyword_token import KEYWORD

class IdentifierToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('IDENTIFIER', value, line, column, previous_token)

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of an identifier token."""
        return char.isalnum() or char == '_'

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid identifier."""

        #An identifier must start with a letter, followed by letters, digits, or underscores

        if not self.value:
            return False
        
        if self.value in KEYWORD.KEYWORDS:
            return False
        
        if not self.value[0].isalpha():
            return False
        
        for char in self.value[1:]:
            if not (char.isalnum() or char == '_'):
                return False
            
        return True
    
    def get_feedback(self):
        """Provides feedback on the token's validity."""
        return "Invalid identifier. Identifiers must start with a letter and can only contain letters, digits, and underscores. Additionally, identifiers cannot be keywords."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid identifier token with more characters."""
        if self.value == '':
            return True
        
        if self.value in KEYWORD.KEYWORDS:
            return False
        
        if not self.value[0].isalpha():
            return False
        
        for char in self.value[1:]:
            if not (char.isalnum() or char == '_'):
                return False
            
        return True
        