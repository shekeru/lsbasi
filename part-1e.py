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

def Parse(Ln):
    while Ln:
        for Ptn, Fn in Lexer:
            V = re.match(r'(?:\s*)('+Ptn+r')(?:\s*)', Ln)
            if V:
                yield Fn(V.group(1))
                Ln = Ln[V.end():]
            else:
                return

def Eval(A, Op, B):
    return Forms[Op](A, B)

while True:
    try:
        Ln = input("scalc> ")
    except EOFError:
        break
    if not Ln:
        continue
    Form = [*Parse(Ln)]
    try:
        Result = Eval(*Form)
        print(Result)
    except TypeError:
        print("Invalid form")
