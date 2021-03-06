import re, operator

Forms = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.__truediv__,
    '%': operator.mod,
}

Lexer = [
    (r'\d+', int),
    (r'[\+*/%-]', str)
]

def GetTokens(Ln):
    while Ln:
        for Ptn, Fn in Lexer:
            V = re.match(r'(?:\s*)('+Ptn+r')(?:\s*)', Ln)
            if V:
                yield Fn(V.group(1))
                Ln = Ln[V.end():]
            else:
                return
            
def Expr(Tokens):
    Value = Term(Tokens)
    while Tokens and Tokens[0] in "+-":
        Value = Forms[Tokens.pop(0)](Value, Term(Tokens))
    return Value

def Term(Tokens):
    Value = Factor(Tokens)
    while Tokens and Tokens[0] in "*/":
        Value = Forms[Tokens.pop(0)](Value, Factor(Tokens))
    return Value

def Factor(Tokens):
    return Tokens.pop(0)

while True:
    try:
        Ln = input("scalc> ")
    except EOFError:
        break
    if not Ln:
        continue
    Tokens = [*GetTokens(Ln)]
    try:
        print(Expr(Tokens))
    except TypeError:
        print("Syntax Error")
    except IndexError:
        print("Unexpected EOF")
