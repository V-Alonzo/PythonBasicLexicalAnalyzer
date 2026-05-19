from Tokens.token import Token

class HexNumberToken(Token):

    def __init__(self, line, column, previous_token = None, value = ""):
        super().__init__('HEX NUMBER', value, line, column, previous_token)

    def verify_current_state(self) -> bool:
        """Checks if the current value is a valid hexadecimal number starting with 0x."""
        if not self.value.startswith("0x"):
            return False
        try:
            int(self.value, 16)
            return True
        except ValueError:
            return False

    def is_valid_char(self, char) -> bool:
        """Checks if a character can be part of a hexadecimal number token."""
        return char.isdigit() or char.lower() in 'abcdefx'
    
    def get_feedback(self):
        """Provides feedback on the token's validity."""
        return "Invalid hexadecimal number. Hexadecimal numbers must start with '0x' followed by digits (0-9) and letters (A-F)."