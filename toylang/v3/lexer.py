import re, operator
# Base Class
class Token:
    def __init__(s, Value):
        s.Value = s.Read(Value)
    def __repr__(s):
        return f"{type(s).__name__}({s.Value})"
    def Read(s, Value):
        return Value
    def Is(s, *Type):
        return any(isinstance(s, x) for x in Type)
class Literal(Token):
    pass
# Useless Tokens
class Comment(Token):
    def __repr__(s):
        return "COMMENT"
class LineBreak(Token):
    def __repr__(s):
        return "_NL"
class LParen(Token):
    def __repr__(s):
        return "LPAREN"
class RParen(Token):
    def __repr__(s):
        return "RPAREN"
# Basic Tokens
class Symbol(Literal):
    def __hash__(s):
        return hash(s.Value)
    def __eq__(s, o):
        if not isinstance(o, Symbol):
            return False
        return s.Value == o.Value
class String(Literal):
    def Read(s, Value):
        return Value[1:-1]
class Integer(Literal):
    def Read(s, Value):
        return int(Value)
class Float(Literal):
    def Read(s, Value):
        return float(Value)
# Assignments
class Strict(Token):
    def __repr__(s):
        return "STRICT"
class Partial(Token):
    def __repr__(s):
        return "PARTIAL"
# Lexing System
Starts = r'(?![,;\=\(\[\d])'
Ends = r'(?<![,;\)\]])'
Lexer = [
    (r'#', Comment),
    (r'[,\r\n]+', LineBreak),
    (r'\-?\d+\.\d+', Float),
    (r'\-?\d+', Integer),
    (r'"(?:[^\\"]|\\.)*"', String),
    (r"\(", LParen), (r"\)", RParen),
    (r">>", Partial), (r'=', Strict),
    (Starts+r'\S+'+Ends, Symbol),
]
# Lexing Functions
def GetTokens(Ln):
    while Ln:
        for Ptn, Fn in Lexer:
            if (V := re.match(r'(?:[^\S\r\n]*)('+ Ptn +r')(?:[^\S\r\n]*)', Ln)):
                yield Fn(V.group(1)); Ln = Ln[V.end():]; break
        else:
            print("Error Lexing, Character:", Ln); break

def Tokenize(Str):
    return [*GetTokens(Str.strip() + "\n")]
# AST 0 Functions
def FindComment(Tokens):
    while Tokens and not ((T := Tokens[0])
        .Is(LineBreak) and T.Value != ","):
        Tokens.pop(0)
# Fuck Comments, Fuck LineBreaks
def CleanLex(Tokens):
    Array = []
    while Tokens:
        if Tokens[0].Is(Comment):
            FindComment(Tokens)
        elif Tokens[0].Is(LineBreak):
            LB = Tokens.pop(0)
            if Array and not Array[-1].Is(LineBreak, Strict, Partial):
                Array.append(LB)
        elif Tokens[0].Is(Strict, Partial):
            if Array and Array[-1].Is(LineBreak):
                Array.pop()
            Array.append(Tokens.pop(0))
        else:
            Array.append(Tokens.pop(0))
    return Array
# Do Stuff
def LexFile(fname):
    Tokens = CleanLex(Tokenize(open(f'code/{fname}.ex').read()))
    print(Tokens); return Tokens
# Run On Example
if "__main__" == __name__:
    LexFile("s1")
