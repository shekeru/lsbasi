import re
INTEGER, EOF = 'INTEGER', 'EOF'
ADD, SUB = "+", "-"
MUL, DIV = "*", "/"

class Token(object):
    def __init__(s, type, value):
        s.type = type
        s.value = value
    def __repr__(s):
        return f"Token({s.type}, {s.value})"

class Interpreter(object):
    def __init__(s, text):
        s.text, s.pos = text, 0
        s.current = None
    def error(s):
        raise Exception("Error parsing input")
    def get_next_token(s):
        if s.pos > len(s.text) -  1:
            return Token(EOF, None)
        char = s.text[s.pos]
        if char.isdigit():
            start = s.pos; end = start + 1
            while s.text[s.pos:end].isdigit() \
                  and end <= len(s.text):
                end += 1
            digits = s.text[s.pos:end - 1]
            s.pos += end - start - 1
            return Token(INTEGER, int(digits))
        if char in "*+-/":
            s.pos += 1
            return Token(char, char)
        if char == " ":
            s.pos += 1
            return s.get_next_token()
        s.error()
    def consume(s, *token_type):
        if s.current.type in token_type:
            s.current = s.get_next_token()
        else:
            s.error()
    def expr(s):
        s.current = s.get_next_token()
        left = s.current
        s.consume(INTEGER)

        op = s.current
        s.consume(ADD, SUB, MUL, DIV)

        right = s.current
        s.consume(INTEGER)

        if op.type == "+":
            result = left.value + right.value
        elif op.type == "-":
            result = left.value - right.value
        elif op.type == "*":
            result = left.value * right.value
        elif op.type == "/":
            result = left.value / right.value
        return result

def main():
    while True:
        try:
            text = input('scalc> ')
        except EOFError:
            break
        if not text:
            continue
        env = Interpreter(text)
        result = env.expr()
        print("->", result)
main()
