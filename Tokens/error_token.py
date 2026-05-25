from Tokens.token import Token

class ErrorToken(Token):

    def __init__(self, line, column, previous_token = None, value = "", feedback = "", should_show_feedback = False):
        super().__init__('ERROR', value, line, column, previous_token)
        self.feedback = feedback
        self.should_show_feedback = should_show_feedback


    def verify_current_state(self) -> bool:
        return None
    
    def is_valid_char(self, char) -> bool:
        return None
    
    def get_feedback(self):
        return self.feedback
    
    def set_feedback(self, feedback: str):
        self.feedback = feedback

    def could_be_valid_token(self):
        return None
    
    def __repr__(self):
        if not self.should_show_feedback:
            return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
    

        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column}, feedback='{self.feedback}')"
    