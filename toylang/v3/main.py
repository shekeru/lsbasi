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

def Eval(Node, Env, Left = False, Body = True):
    if isinstance(Node, Strict):
        Hd, *Bdy = [Eval(x, Env, Left, Body) for x in Node]
        for I, K in enumerate(Bdy):
            if Body and isinstance(K, Symbol) and '*' == K.Value[0]:
                K.Value = K.Value[1:]; Bdy = [*Bdy[:I],
                    *Eval(K, Env, Left, Body), *Bdy[I + 1:]]
                break
        if callable(Hd):
            return Hd(*Bdy)
        if isinstance(Hd, tuple):
            return FunctionCall(*Hd[1](Bdy), Env)
        if isinstance(Hd, Function):
            return FunctionCall(Hd, Bdy, Env)
        if not Bdy:
            return Hd
        return Node
    if isinstance(Node, Partial):
        if len(Node) > 1:
            return Eval(Strict(Node), Env, Left, Body)
        return Eval(Node[0], Env)
    if isinstance(Node, Assignment):
        LVal, RVal = Node
        LVal = Eval(LVal, Env, True, Body)
        RVal = Eval(RVal, Env, Left, Body)
        if isinstance(RVal, Partial):
            RVal = RVal[0]
        Env[LVal] = RVal; return RVal
    if isinstance(Node, MatchFunction):
        Options = [Eval(x, Env, Left, Body) for x in Node]
        def ResolveFunction(Args):
            for Func in Options:
                J, Params = -1, Func[:-1]
                for I, P in enumerate(Params):
                    if isinstance(P, Symbol) and P.Value[0] == "*":
                        P.Value = P.Value[1:]; J = I; break
                if J >= 0:
                    Args[J] = Args[J:]
                    Args = Args[:J+1]
                for Req, Is in zip(Params, Args):
                    if not isinstance(Req, Symbol) and Req.Value != Is:
                        break
                else:
                    return Func, Args
        return "lol", ResolveFunction
    if isinstance(Node, Function):
        return Node
    if isinstance(Node, Symbol):
        return Node if Left else Env.Find(Node)
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
