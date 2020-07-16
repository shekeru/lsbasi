INTEGER, EOF = 'INTEGER', 'EOF'
PLUS, MINUS = 'PLUS', 'MINUS'
MUL, DIV = 'MUL', 'DIV'
OPS = (PLUS, MINUS, MUL, DIV)

class Token(object):
    def __init__(s, type, value):
        s.type = type
        s.value = value
    def __repr__(s):
        return f"Token({type}, {value})"
    def __str__(s):
        return repr(s)

class Lexer(object):
    def __init__(s, text):
        s.text, s.pos = text, 0
        s.char = s.text[s.pos]
    def error(s):
        raise Exception("Invalid lexing")
    def skip_whitespace(s):
        while s.char and s.char.isspace():
            s.advance()
    def advance(s):
        s.pos += 1
        if s.pos >= len(s.text):
            s.char = None
        else:
            s.char = s.text[s.pos]
    def integer(s):
        result = ''
        while s.char and s.char.isdigit():
            result += s.char
            s.advance()
        return int(result)
    def get_next_token(s):
        while s.char:
            if s.char.isspace():
                s.skip_whitespace()
                continue
            if s.char.isdigit():
                return Token(INTEGER, s.integer())
            if s.char == "+":
                s.advance()
                return Token(PLUS, '+')
            if s.char == "-":
                s.advance()
                return Token(MINUS, '-')
            if s.char == "*":
                s.advance()
                return Token(MUL, '*')
            if s.char == "/":
                s.advance()
                return Token(DIV, '/')
            s.error()
        return Token(EOF, None)
    
class Interpreter(object):
    def __init__(s, lexer):
        s.lexer = lexer
    def error(s):
        raise Exception("Invalid syntax")
    def eat(s, t_type):
        if s.token.type == t_type:
            s.token = s.lexer.get_next_token()
        else:
            s.error()
    def factor(s):
        token = s.token
        s.eat(INTEGER)
        return token.value
    def expr(s):
        s.token = s.lexer.get_next_token()
        result = s.factor()
        while s.token.type in OPS:
            token = s.token
            if token.type == MUL:
                s.eat(MUL)
                result *= s.factor()
            elif token.type == DIV:
                s.eat(DIV)
                result /= s.factor()
            elif token.type == MINUS:
                s.eat(MINUS)
                result -= s.factor()
            elif token.type == PLUS:
                s.eat(PLUS)
                result += s.factor()
        return result
    
while True:
    try:
        text = input("calc> ")
    except EOFError:
        break
    if not text:
        continue
    try:
        terms = Lexer(text)
        model = Interpreter(terms)
        result = model.expr()
        print(result)
    except Exception as e:
        print(e)


            
