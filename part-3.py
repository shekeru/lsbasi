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

class Interpreter(object):
    def __init__(s, text):
        s.text, s.pos = text, 0
        s.cur_char = s.text[s.pos]
        s.cur_token = None
    def error(s):
        raise Exception("Error parsing input")
    def advance(s):
        s.pos += 1
        if s.pos >= len(s.text):
            s.cur_char = None
        else:
            s.cur_char = s.text[s.pos]
    def skip_whitespace(s):
        while s.cur_char and s.cur_char.isspace():
            s.advance()
    def integer(s):
        result = ''
        while s.cur_char and s.cur_char.isdigit():
            result += s.cur_char
            s.advance()
        return int(result)
    def get_next_token(s):
        while s.cur_char:
            if s.cur_char.isspace():
                s.skip_whitespace()
                continue
            if s.cur_char.isdigit():
                return Token(INTEGER, s.integer())
            if s.cur_char == "+":
                s.advance()
                return Token(PLUS, '+')
            if s.cur_char == "-":
                s.advance()
                return Token(MINUS, '-')
            if s.cur_char == "*":
                s.advance()
                return Token(MUL, '*')
            if s.cur_char == "/":
                s.advance()
                return Token(DIV, '/')
            self.error()
        return Token(EOF, None)
    def eat(s, t_type):
        if s.cur_token.type == t_type:
            s.cur_token = s.get_next_token()
        else:
            s.error()
    def term(s):
        token = s.cur_token
        s.eat(INTEGER)
        return token.value
    def expr(s):
        s.cur_token = s.get_next_token()

        result = s.term()
        while s.cur_token.type in (PLUS, MINUS):
            token = s.cur_token
            if token.type == PLUS:
                s.eat(PLUS)
                result += s.term()
            elif token.type == MINUS:
                s.eat(MINUS)
                result -= s.term()
        return result
    
while True:
    try:
        text = input("calc> ")
    except EOFError:
        break
    if not text:
        continue
    statement = Interpreter(text)
    result = statement.expr()
    print(result)


            
