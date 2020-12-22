class Symbol(str):
    def __repr__(s):
        return f'Symbol({eval(super().__repr__())})'

class Function:
    def __init__(s, Terms):
        s.Args, s.Body = Terms[:-1], Terms[-1]

class EnvS(dict):
    def __init__(s, Parent = None):
        super().__init__()
        s.Parent = Parent
    def Find(s, Var):
        if Var in s:
            return s
        if s.Parent != None:
            return s.Parent.Find(Var)
