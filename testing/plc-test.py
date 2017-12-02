# Test the functionality of how PLC works

from ply import lex, yacc

# List of token names.   This is always required
tokens = (
    'HEADER',
    'FIRSTID',
    'TITLE'
)

# Regular expression rules for simple tokens
t_HEADER = r'Recommendation.*|Recommendations.*'
t_FIRSTID = r'\d+(?=\n\n\[)'
t_TITLE = r'(?<=\n\[)[^\]]+'


# Error handling rule
def t_error(t):
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
file = open("minutes.txt", "r")
data = file.read()
file.close()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

