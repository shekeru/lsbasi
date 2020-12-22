import re, operator
# Base Class
class Token:
    def __init__(s, Value):
        s.Value = s.Read(Value)
    def __repr__(s):
        return f"{type(s).__name__}({s.Value})"
    def Read(s, Value):
        return Value
# Expressions
class Expr(Token):
    pass

class String(Expr):
    def Read(s, Value):
        return Value[1:-1]

class Integer(Expr):
    def Read(s, Value):
        return int(Value)

class Float(Expr):
    def Read(s, Value):
        return float(Value)

class Symbol(Expr):
    pass
# Lexer Utility
class LParen(Token):
    def __repr__(s):
        return "LPAREN"

class RParen(Token):
    def __repr__(s):
        return "RPAREN"
    
class LPart(Token):
    def __repr__(s):
        return "LPART"

class RPart(Token):
    def __repr__(s):
        return "RPART"
    
class LineBreak(Token):
    def __repr__(s):
        return "_NL"

class Comment(Token):
    def __repr__(s):
        return "COMMENT"

class Assign(Token):
    def __repr__(s):
        return f"ASSIGN"

class Start(Token):
    def __repr__(s):
        return "START"

class End(Token):
    def __repr__(s):
        return "END"

class Func(Token):
    def __repr__(s):
        return "LAMBDA"
# Lexing Rules
Starts = r'(?![;\=\(\[\d])'
Ends = r'(?<![;\)\]])'
Lexer = [
    (r'#', Comment),
    (r"=", Assign), (r"fn", Func),
    (r"->", Start), (r"end", End),
    (r"\[", LPart), (r"\]", RPart),
    (r"\(", LParen), (r"\)", RParen),
    (r'[;\r\n]+', LineBreak),
    (r'"[\S\s]+"', String),
    (r'\-?\d+\.\d+', Float),
    (r'\-?\d+', Integer),
    (Starts+r'\S+'+Ends, Symbol),
]
# Lexing Functions
def GetTokens(Ln):
    while Ln:
        for Ptn, Fn in Lexer:
            if (V := re.match(r'(?:[^\S\r\n]*)('+ Ptn +r')(?:[^\S\r\n]*)', Ln)):
                yield Fn(V.group(1)); Ln = Ln[V.end():]; break
        else:
            print("Error Parsing:", Ln); break

def Tokenize(Str):
    return [*GetTokens(Str.strip() + "\n")]
# AST 1 Classes
class Section(list):
    def __init__(s, Exprs):
        super().__init__(Exprs)
    def __repr__(s):
        return f"{type(s).__name__}{super().__repr__()}"

class Partial(Section):
    pass
    
class Strict(Section):
    pass
# Ast 2 Classes
class Statement(Section):
    pass
# Ast 3 Classes
class Assignment(Section):
    pass

class StmntBlock(Section):
    pass

class Function(Section):
    pass
# AST 1 Functions
def ChewLines(Tokens):
    while Tokens and isinstance(Tokens[0], LineBreak):
        Tokens.pop(0)
def FindComment(Tokens):
    while Tokens and not isinstance(Tokens[0], LineBreak):
        Tokens.pop(0)

def FindFunction(Tokens):
    Tokens.pop(0); ChewLines(Tokens)
    List, Body = Function([]), StmntBlock([])
    while Tokens and isinstance(Tokens[0], Symbol):
        List.append(Tokens.pop(0))
    ChewLines(Tokens)
    if Tokens and isinstance(Tokens.pop(0), Start):
        ChewLines(Tokens)
        while Tokens and not isinstance(Tokens[0], End) \
            and not isinstance(Tokens[0], LineBreak):
            Body.append(FindImpStrict(Tokens))
        List.append(Body); ChewLines(Tokens); Tokens.pop(0)
    return List

def FindImpStrict(Tokens):
    List = Strict([])
    while Tokens:
        if isinstance(Tokens[0], Expr):
            List.append(Tokens.pop(0))
        elif isinstance(Tokens[0], LParen):
            Tokens.pop(0)
            List.append(FindImpStrict(Tokens))
            Tokens.pop(0)
        elif isinstance(Tokens[0], LPart):
            List.append(FindPartial(Tokens))
        else:
            if isinstance(List[0], Strict) and len(List) == 1:
                List = List[0]
            return List

def FindPartial(Tokens):
    List = Partial([]); Tokens.pop(0)
    while Tokens:
        if isinstance(Tokens[0], Expr) or isinstance(Tokens[0], LParen):
            List.append(Partial(FindImpStrict(Tokens)))
        elif isinstance(Tokens[0], RPart):
            if isinstance(List[0], Partial) and len(List) == 1:
                List = List[0]
            Tokens.pop(0); return List
        else:
            print("Error, Missing ]")
# Identify Stricts/Partials, Remove Comments
def ParseTree1(Tokens):
    Array = []
    while Tokens:
        # Expressions
        if isinstance(Tokens[0], Expr) or isinstance(Tokens[0], LParen):
            Array.append(FindImpStrict(Tokens))
        elif isinstance(Tokens[0], LPart):
            Array.append(FindPartial(Tokens))
        # Functions
        elif isinstance(Tokens[0], Func):
            Array.append(FindFunction(Tokens))
        # Ignore These
        elif isinstance(Tokens[0], Comment):
            FindComment(Tokens)
        elif isinstance(Tokens[0], LineBreak):
            LB = Tokens.pop(0)
            if Array and not isinstance(Array[-1], LineBreak) \
               and not isinstance(Array[-1], Assign):
                Array.append(LB)
        # Disregard LineBreaks
        elif isinstance(Tokens[0], Assign):
            if Array and isinstance(Array[-1], LineBreak):
                Array.pop()
            Array.append(Tokens.pop(0))
        # Leave These
        else:
            Array.append(Tokens.pop(0))
    return Array
# Combine Stricts/Partials into Statements, Remove Lines?
def FindStatement(Tokens):
    List = Statement([])
    while Tokens and isinstance(Tokens[0], Section):
        List.append(Tokens.pop(0))
    return List
def ParseTree2(Tokens):
    Array = []
    while Tokens:
        if isinstance(Tokens[0], Section):
            Array.append(FindStatement(Tokens))
        else:
            Array.append(Tokens.pop(0))
    return Array
# Do Stuff
T0 = Tokenize(open('code/t2.ex').read())
print(T0)
print("------------------------")
for Ln in (T1 := ParseTree1(T0)):
    print(Ln)
print("------------------------")
#for Ln in (T2 := ParseTree2(T1)):
    #print(Ln)
