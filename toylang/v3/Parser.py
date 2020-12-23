from Lexer import *
# AST Classes
class Section(list, Token):
    def __init__(s, Exprs):
        super().__init__(Exprs)
    def __repr__(s):
        return f"{type(s).__name__}{super().__repr__()}"
class Expression(Section):
    pass
class Assignment(Section):
    pass
# Parsing Functions
def ParseExpression(Tokens):
    Array = []
    while Tokens:
        if Tokens[0].Is(Literal):
            Array.append(Tokens.pop(0))
        elif Tokens[0].Is(LParen):
            Tokens.pop(0)
            Array.append(ParseExpression(Tokens))
            Tokens.pop(0)
        elif Tokens[0].Is(Strict, Partial):
            return Assignment([Array[-1],
                Tokens.pop(0), ParseExpression(Tokens)])
        else:
            break
    # Un-nested Expressions
    if len(Array) == 1 and Array[0].Is(Expression):
        return Array[0]
    return Expression(Array)    
def ParseProgram(Tokens):
    Array = []
    while Tokens:
        if not Tokens[0].Is(LineBreak):
            Array.append(ParseExpression(Tokens))
        else:
            Tokens.pop(0)
    return Array
# Return AST
def ReadAST(fname):
    T = LexFile(fname)
    P = ParseProgram(T)
    print("--------------")
    for Ln in P:
        print(Ln)
    return P
# Run if Main
if "__main__" == __name__:
    ReadAST("s1")
