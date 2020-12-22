from stdlib import Globals
from syntax import Parse
from structs import *

def Eval(Node, Env):
    if Node.data == "fn":
        return Function([Eval(X, Env) for X in Node.children])
    if Node.data == "strict":
        Hd, *Xs = [Eval(X, Env) for X in Node.children]
        return Hd(*Xs) if Xs else Hd
    if Node.data == "assign":
        Left, Right = [Eval(X, Env) for X in Node.children]
        print(Left, Env)
        Env[Left] = Right; return Right
    if Node.data in ("stmnt", "expr"):
        return Eval(Node.children[0], Env)
    if Node.data == "integer":
        return int(Node.children[0])
    if Node.data == "symbol":
        return Symbol(Node.children[0])
    if Node.data == "string":
        return Node.children[0]
    if Node.data == "block":
        return Node.children
    print(Node)

pp = Parse("t1.ex")
print(pp.pretty())
# Evaluate Program
Value, Env = None, EnvS(Globals)
for Stmnt in pp.children:
    Value = Eval(Stmnt, Env)
print(Value, Env)
