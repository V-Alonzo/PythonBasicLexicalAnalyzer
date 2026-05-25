from enum import Enum
from abc import ABC, abstractmethod

class Token(ABC):

    def __init__(self, type, value, line, column, previous_token = None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
        self.reachedCompleteState = False
        self.previous_token = previous_token

    @abstractmethod
    def verify_current_state(self) -> bool:
        """Every token must implement this method to determine if the current value is valid for its type."""
        pass

    def check_validity_token(self) -> bool:
        """Checks if the current value forms a valid token."""
        if self.verify_current_state():
            self.reachedCompleteState = True
            return True
        else:
            self.reachedCompleteState = False
            return False
        
    def append_char(self, char):
        """Appends a character to the token's value and checks if it still forms a valid token."""
        
        self.value += char
        return self.verify_current_state()
    
    @abstractmethod
    def could_be_valid_token(self) -> bool:
        """Checks if the current value could still potentially form a valid token with more characters."""
        pass
    
    @abstractmethod
    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of the token's value."""
        # This method can be overridden by specific token types to define valid characters
        pass

    @abstractmethod
    def get_feedback(self):
        """Provides feedback on the token's validity."""
        pass

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
