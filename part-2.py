INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'
MUL, DIV = 'MUL', 'DIV'

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
    def eat(s, t_type):
        if s.cur_token.type == t_type:
            s.cur_token = s.get_next_token()
        else:
            s.error()
    def expr(s):
        s.cur_token = s.get_next_token()

        left = s.cur_token
        s.eat(INTEGER)

        op = s.cur_token
        if op.type != INTEGER:
            s.eat(op.type)

        right = s.cur_token
        s.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == MUL:
            result = left.value * right.value
        elif op.type == DIV:
            result = left.value / right.value
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


            
