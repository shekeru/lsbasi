from Parser import *
# Data Structure
class EnvS(dict):
    def __init__(s, Parent = None):
        super().__init__()
        s.Parent = Parent
    def Find(s, Var):
        if Var in s:
            return s
        if s.Parent != None:
            return s.Parent.Find(Var)
# Evaluate Line
def Eval(Node, Env):
    if Node.Is(Expression):
        if Node.Lazy:
            if len(Node) == 1:
                Node = Node[0]
            return Node
        # Normal Eval
        Hd, *Bdy = [Eval(x, Env) for x in Node]
        if callable(Hd):
            return Hd(*Bdy)
        if isinstance(Hd, Expression):
            return Eval(Hd, Env)
        return Hd
    if Node.Is(Assignment):
        Left, Right = Node
        Left = Eval(Left, Env)
        Right = Eval(Right, Env)
        if isinstance(Right, Expression) and Right.Lazy:
            Right.Lazy = False
        Env[Left] = Right; return Right
    if (Start := Node).Is(Reference):
        if Start.Level:
            while isinstance(Node, Symbol):
                Next = Env.Find(Node).get(Node, Node)
                if Next == Node or not isinstance(Next, Symbol):
                    return Node
                Node = Next
        return Symbol(Node.Value)
    if Node.Is(Symbol):
        while Node:
            Next = (Dt := Env.Find(Node)).get(Node, Node)
            if Next != Node and not isinstance(Next, Symbol):
                return Next
            elif Next == Node:
                return Node
            Node = Next
    if Node.Is(Integer):
        return Node.Value
    if Node.Is(Float):
        return Node.Value
    if Node.Is(String):
        return Node.Value
    print("unknown token", Node)
# Prelude, Globals
Globals, V = EnvS(), None
def Std_Puts(*xs):
    print(*xs)
    return xs if len(xs) > 1 else xs[0]
Globals[Symbol('show')] = Std_Puts
# Run Program
Lines = ReadAST("s1")
for Stmnt in Lines:
    V = Eval(Stmnt, Globals)
print(">>>", V, Globals)
