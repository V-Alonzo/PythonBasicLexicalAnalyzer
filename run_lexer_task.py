import sys
from Lexer import Lexer

source = '''int total = 0 ;
float average = 3.5 ;
if ( total <= 10 && ! done ) {
message = "hola ; mundo" ;
total = total + 1 - 2 * 3 / 4 ;
badId$ = 7 ;
badHex = 0xG1 ;
badNumber = 3.14d ;
check === != >= <= , return ;
} else {
while ( total != 0 ) {
total = total - 1 ;
}
logic = & ;
}
'''

lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    feedback = getattr(token, "feedback", None)
    print(f"('{token.type}', r'{token.value}', {token.line}, {token.column}, {feedback})")
