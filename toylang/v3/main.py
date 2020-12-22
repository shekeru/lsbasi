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

def FunctionCall(Fn, Args, Env):
    Local, V = EnvS(Env), None
    Params, Block = Fn[:-1], Fn[-1]
    Local.update(zip(Params, Args))
    for Stmnt in Block:
        V = Eval(Stmnt, Local)
    return V

def Eval(Node, Env):
    if isinstance(Node, Strict):
        Hd, *Bdy = [Eval(x, Env) for x in Node]
        if callable(Hd):
            return Hd(*Bdy)
        if isinstance(Hd, tuple):
            return FunctionCall(Hd[1](Bdy), Bdy, Env)
        if isinstance(Hd, Function):
            return FunctionCall(Hd, Bdy, Env)
        return Hd
    if isinstance(Node, Partial):
        if len(Node) > 1:
            0 / 0
        return Eval(Node[0], Env)
    if isinstance(Node, Assignment):
        Left, Right = [Eval(x, Env) for x in Node]
        if isinstance(Right, Partial):
            Right = Right[0]
        Env[Left] = Right; return Right
    if isinstance(Node, MatchFunction):
        Options = [Eval(x, Env) for x in Node]
        def ResolveFunction(Args):
            for Func in Options:
                Params = Func[:-1]
                for Req, Is in zip(Params, Args):
                    if not isinstance(Req, Symbol) and Req.Value != Is:
                        break
                else:
                    return Func
        return "lol", ResolveFunction
    if isinstance(Node, Function):
        return Node
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
Globals[Symbol('show')] = Std_Puts
Globals[Symbol('add')] = lambda *xs: sum(xs)
for Stmnt in Lines:
    V = Eval(Stmnt, Globals)
print(">>>", V)
