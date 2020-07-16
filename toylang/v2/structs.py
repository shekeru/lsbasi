from stdlib import Globals, Symbol

class Block(dict):
    def __init__(s):
        s.Name, s.Body = "", []
    def __repr__(s):
        return f"{s.Name}:{type(s)}"
    def Find(s, Var):
        if Var in s:
            return s
        if s.Parent != None:
           return s.Parent.Find(Var)
    def Execute(s, Terms):
        V = None
        for Term in Terms:
            V = s.Eval(Term)
        return V
    def Eval(s, Term):
        if isinstance(Term, Symbol):
            return s.Find(Term)[Term]
        if isinstance(Term, list):
            # Special Forms
            if Term[0] == Symbol('set!'):
                _, Name, Exp = Term
                Where = s.Find(Name) or s
                Where[Name] = s.Eval(Exp)
                return Where[Name]
            # Normal Forms
            Op, *Exp = [s.Eval(Ref) for Ref in Term]
            return Op.Call(*Exp)
        return Term

class Program(Block):
    def __init__(s, StdLib):
        super().__init__()
        s.update(StdLib)
        s.Parent = None

class Function(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Params = []
    def Call(s, *Args):
        s.update(dict(zip(s.Params, Args)))
        return s.Execute(s.Body)

class While(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Cond = []
    def Call(s):
        while s.Eval(s.Cond):
            V = s.Execute(s.Body)
        return V

class If(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Cond = []
        s.Other = []
    def Call(s):
        if s.Eval(s.Cond):
            V = s.Execute(s.Body)
        else:
            V = s.Execute(s.Other)
        return V
