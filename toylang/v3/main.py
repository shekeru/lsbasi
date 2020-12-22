from lexer import *
Lines = RealParse("t1")

class EnvS(dict):
    def __init__(s, Parent = None):
        super().__init__()
        s.Parent = Parent
    def Find(s, Var):
        if Var in s:
            return s[Var]
        if s.Parent != None:
            return s.Parent.Find(Var)
        return Var

def Eval(Node, Env):
    if isinstance(Node, Strict):
        if len(Node) > 1:
            Hd, *Bdy = [Eval(x, Env) for x in Node]
            return Hd(*Bdy)
        else:
            return Eval(Node[0], Env)
    if isinstance(Node, Function):
        Parts = [Eval(x, Env) for x in Node]
    if isinstance(Node, Assignment):
        Left, Right = [Eval(x, Env) for x in Node]
        Env[Left] = Right
    if isinstance(Node, Symbol):
        return Env.Find(Node)
    if isinstance(Node, Integer):
        return Node.Value
    if isinstance(Node, Float):
        return Node.Value
    if isinstance(Node, String):
        return Node.Value

Globals, V = EnvS(), None
def Std_Puts(*xs):
    print(*xs)
    return xs if len(xs) > 1 else xs[0]
Globals[Symbol('puts')] = Std_Puts
for Stmnt in Lines:
    V = Eval(Stmnt, Globals)
print(">>>", V)
