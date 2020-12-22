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
    def __hash__(s):
        return hash(s.Value)
    def __eq__(s, o):
        return s.Value == o.Value
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
    (r'[\r\n]+', LineBreak),
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
# AST 0 Functions
def ChewLines(Tokens):
    while Tokens and isinstance(Tokens[0], LineBreak):
        Tokens.pop(0)
def FindComment(Tokens):
    while Tokens and not isinstance(Tokens[0], LineBreak):
        Tokens.pop(0)
# Ast 1 Functions
def FindFunction(Tokens):
    Tokens.pop(0); ChewLines(Tokens)
    List, Body = Function([]), StmntBlock([])
    while Tokens and isinstance(Tokens[0], Symbol):
        List.append(Tokens.pop(0))
    ChewLines(Tokens)
    if Tokens and isinstance(Tokens.pop(0), Start):
        ChewLines(Tokens)
        while Tokens and not isinstance(Tokens[0], End):
            Body.append(FindImpStrict(Tokens)); ChewLines(Tokens);
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
        elif isinstance(Tokens[0], Func):
            List.append(FindFunction(Tokens))
        elif isinstance(Tokens[0], Assign):
            Tokens.pop(0); V = [List.pop(), FindPartial(Tokens)
                if isinstance(Tokens[0], LPart) else FindImpStrict(Tokens)]
            List.append(Assignment(V)); return List
        else:
            break
    if len(List) == 1 and isinstance(List[0], Strict):
        List = List[0]
    return List

def FindPartial(Tokens):
    List = Partial([])
    while Tokens:
        if isinstance(Tokens[0], Expr):
            List.append(Tokens.pop(0))
        elif isinstance(Tokens[0], LParen):
            if len(V := FindImpStrict(Tokens)) > 1:
                List += V
            else:
                List.append(V)
        elif isinstance(Tokens[0], LPart):
            Tokens.pop(0)
            List.append(FindPartial(Tokens))
            Tokens.pop(0)
        elif isinstance(Tokens[0], Assign):
            Tokens.pop(0); V = [List.pop(), FindPartial(Tokens)
                if isinstance(Tokens[0], LPart) else FindImpStrict(Tokens)]
            List.append(Assignment(V)); return List
        else:
            break
    if len(List) == 1 and isinstance(List[0], Partial):
        List = List[0]
    return List
# Fuck Comments, Fuck LineBreaks
def CleanLex(Tokens):
    Array = []
    while Tokens:
        if isinstance(Tokens[0], Comment):
            FindComment(Tokens)
        elif isinstance(Tokens[0], LineBreak):
            LB = Tokens.pop(0)
            if Array and not isinstance(Array[-1], LineBreak) \
               and not isinstance(Array[-1], Assign):
                Array.append(LB)
        elif isinstance(Tokens[0], Assign):
            if Array and isinstance(Array[-1], LineBreak):
                Array.pop()
            Array.append(Tokens.pop(0))
        else:
            Array.append(Tokens.pop(0))
    return Array
# Everything is Either Strict or Partial
def ParseTree(Tokens):
    Array = []
    while Tokens:
        if not isinstance(Tokens[0], LineBreak):
            Array.append(FindImpStrict(Tokens))
        else:
            Tokens.pop(0)
    return Array
# Do Stuff
def RealParse(fname):
    Tokens = CleanLex(Tokenize(open(f'code/{fname}.ex').read()))
    print(Tokens)
    print("------------------------")
    for Ln in (Stmnts := ParseTree(Tokens)):
        print(Ln)
    print("------------------------")
    return Stmnts
