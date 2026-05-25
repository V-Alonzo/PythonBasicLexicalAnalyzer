from Tokens.token import Token

class LogicalToken(Token):

    operators = {
        "&&":"AND",
        "||":"OR",
        "!":"NOT"
    }

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('LOGICAL', value, line, column, previous_token)
        self.verify_current_state()

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid logical operator."""
        if self.value in self.operators:
            self.type = self.operators[self.value]
            return True
        
        return False
    
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a logical operator token."""
        return char in self.operators
    
    def get_feedback(self):
        return f"Invalid logical operator."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid logical operator token with more characters."""
        return self.value == '' or any(operator.startswith(self.value) and len(operator) > len(self.value) for operator in self.operators)
