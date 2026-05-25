from Tokens.token import Token

class EOFToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('EOF', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        return None
    
    def is_valid_char(self, char) -> bool:
        return None
    
    def get_feedback(self):
        return "End of file reached. No more tokens to process."
    
    def could_be_valid_token(self) -> bool:
        return None
