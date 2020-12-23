from Lexer import *
# Special Tokens
class Reference(Symbol):
    def __init__(s, Sym):
        super().__init__(Sym.Value)
        s.Level = 0
    def __repr__(s):
        return f"VarRef({s.Level}, {s.Value})"
# AST Classes
class Section(list, Token):
    def __init__(s, Exprs):
        super().__init__(Exprs)
    def __repr__(s):
        return f"{type(s).__name__}{super().__repr__()}"
    def Is(s, *Type):
        return any(isinstance(s, x) for x in Type)
class Expression(Section):
    def __init__(s, Exprs):
        super().__init__(Exprs)
        s.Lazy = False
    def __repr__(s):
        return ("Lazy" if s.Lazy else "Strict")+f"{super().__repr__()}"
class Assignment(Section):
    pass
# Parsing Functions
def LVal(VarRef):
    if "*" == VarRef.Value[0]:
        VarRef.Level += 1
        VarRef.Value = VarRef.Value[1:]
        return LVal(VarRef)
    return VarRef
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
            Type = Tokens.pop(0).Is(Partial)
            RVal = ParseExpression(Tokens); RVal.Lazy = Type
            return Assignment([LVal(Reference(Array[-1])), RVal])
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
    print("--------------")
    return P
# Run if Main
if "__main__" == __name__:
    ReadAST("s1")
