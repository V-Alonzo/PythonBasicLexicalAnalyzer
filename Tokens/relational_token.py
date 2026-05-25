from Tokens.token import Token

class RelationalToken(Token):

    relational_operators = {
        '<': 'LESS_THAN',
        '<=': 'LESS_THAN_EQUAL',
        '>': 'GREATER_THAN',
        '>=': 'GREATER_THAN_EQUAL',
        '==': 'EQUAL',
        '===': 'STRICT_EQUAL',
        '!=': 'NOT_EQUAL'
    }

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('RELATIONAL', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid relational operator."""
        if self.value in self.relational_operators:
            self.type = self.relational_operators[self.value]
            return True
        return False

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a relational operator."""
        return char in ['<', '>', '=', '!']
    
    def get_feedback(self):
        return f"Invalid relational operator."
    
    def could_be_valid_token(self):
        """Checks if the current value could still potentially form a valid relational operator token with more characters."""
        return self.value == '' or any(operator.startswith(self.value) and len(operator) >= len(self.value) for operator in self.relational_operators)