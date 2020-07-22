class ReturnExcept(Exception):
    pass

class Block(dict):
    def __init__(s, Parent = None):
        s.Name, s.Body = "", []
        s.Parent = Parent
    def __repr__(s):
        return f"{s.Name}:{type(s)}"
    def Find(s, Var):
        if Var in s:
            return s
        if s.Parent != None:
            return s.Parent.Find(Var)
    def Execute(s, Terms, L_Args = {}):
        V = None
        for Term in Terms:
            V = s.Eval(Term, L_Args)
        return V
    def Eval(s, Term, L_Args = {}):
        if isinstance(Term, Symbol):
            if Term in L_Args:
                return L_Args[Term]
            return s.Find(Term)[Term]
        if isinstance(Term, list):
            # Special Forms
            if Term[0] == Symbol('ret!'):
                Value = s.Eval(Term[1:], L_Args)
                raise ReturnExcept(Value)
            if Term[0] == Symbol('set!'):
                _, Name, Exp = Term
                Where = s.Find(Name) or s
                Where[Name] = s.Eval(Exp, L_Args)
                return Where[Name]
            # Normal Forms
            Op, *Exp = [s.Eval(Ref, L_Args) for Ref in Term]
            if isinstance(Op, Block):
                return Op.Call(*Exp, L_Args = L_Args)
            if not Exp:
                return Op
        return Term

class Program(Block):
    def __init__(s, StdLib):
        super().__init__(None)
        s.update(StdLib)

class Function(Block):
    def __init__(s, Parent):
        super().__init__(Parent)
        s.Params = []
    def Call(s, *Args, L_Args = {}):
        L_Args = dict(zip(s.Params, Args))
        try:
            return s.Execute(s.Body, L_Args)
        except ReturnExcept as Ev:
            return Ev

class While(Block):
    def __init__(s, Parent):
        super().__init__(Parent)
        s.Cond = []
    def Call(s, L_Args = {}):
        while s.Eval(s.Cond, L_Args):
            V = s.Execute(s.Body, L_Args)
        return V

class If(Block):
    def __init__(s, Parent):
        super().__init__(Parent)
        s.Cond, s.Other = [], []
    def Call(s, L_Args = {}):
        if s.Eval(s.Cond, L_Args):
            V = s.Execute(s.Body, L_Args)
        else:
            V = s.Execute(s.Other, L_Args)
        return V

class Condition(Block):
    def __init__(s, Parent):
        super().__init__(Parent)
        s.Tests, s.Other = [], []
    def Call(s, L_Args = {}):
        for x in range(len(s.Tests)):
            if s.Eval(s.Tests[x], L_Args):
                return s.Execute(s.Body[x], L_Args)
        return s.Execute(s.Other, L_Args)

class Symbol(str):
    def __repr__(s):
        return f'Symbol({eval(super().__repr__())})'
    def __str__(s):
        return repr(s)
