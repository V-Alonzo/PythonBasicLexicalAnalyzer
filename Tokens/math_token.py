from Tokens.token import Token

class MathToken(Token):

    operators = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '%': 'MODULO',
        '++' : 'INCREMENT',
        '--' : 'DECREMENT'
    }

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('MATH', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid math sign."""
        if self.value in self.operators:
            self.type = self.operators[self.value]
            return True
        return False

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a math token."""
        return char in self.operators
    
    def get_feedback(self):
        return f"Invalid math operator."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid math token with more characters."""
        return self.value == '' or self.value in self.operators
