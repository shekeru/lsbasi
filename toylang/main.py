from stdlib import Globals, Symbol
from syntax import Parse

def Eval(Term, Locals):
    # Atom
    if not isinstance(Term, list):
        if Term in Locals:
            return Locals[Term]
        if Term in Globals:
            return Globals[Term]
        return Term
    # List Expression
    Array = []
    for Ref in Term:
        if isinstance(Ref, list):
            Array.append(Eval(Ref, Locals))
        elif Ref in Locals:
            Array.append(Locals[Ref])
        elif Ref in Globals:
            Array.append(Globals[Ref])
        else:
            Array.append(Ref)
    Op, *Exp = Array
    # Special Forms
    if Op == Symbol('set!'):
        Locals[Term[1]] = Exp[1]
        return Locals[Term[1]]
    # Statement Blocks
    if isinstance(Op, While) or isinstance(Op, If):
        return Op.Handle(Locals)
    if isinstance(Op, int) and not len(Exp):
        return Op
    if Op is not None:
        return Op.Call(*Exp)        
    #print("Missed:", Term, Array)

class Block:
    def __init__(s):
        s.Body = []
        s.Vars = {}
    def Execute(s, Terms, Locals):
        V = None
        s.retFlag = False
        for Term in Terms:
            if Term[0] == Symbol("ret!"):
                V = Eval(Term[1:], Locals)
                s.SignalReturn(s.Parent)
                return V
            V = Eval(Term, Locals)
            if s.retFlag:
                break
        return V
    def SignalReturn(s, Pr):
        if isinstance(Pr, Function):
            Pr.retFlag = True
        else:
            s.SignalReturn(Pr.Parent)

class Program(Block):
    def __init__(s):
        super().__init__()

class Function(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Params = []
    def Call(s, *Args):
        Locals = dict(zip(s.Params, Args))
        return s.Execute(s.Body, Locals)

class While(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Cond = []
    def Handle(s, Locals):
        while Eval(s.Cond, Locals):
            V = s.Execute(s.Body, Locals)
        return V

class If(Block):
    def __init__(s, Parent):
        super().__init__()
        s.Parent = Parent
        s.Cond = []
        s.Other = []
    def Handle(s, Locals):
        if Eval(s.Cond, Locals):
            V = s.Execute(s.Body, Locals)
        else:
            V = s.Execute(s.Other, Locals)
        return V
            

def Dispatch(Node, Env = None):
    if Node.data == "start":
        Env = Program()
        for El in Node.children:
            Dispatch(El, Env)
        return Env
    if Node.data == "function":
        Env = Function(Env)
        Name, Params, Body = Node.children
        Env.Name = Dispatch(Name, Env)
        Env.Params = Dispatch(Params, Env)
        Env.Body = Dispatch(Body, Env)
        Globals[Env.Name] = Env
        return Env
    if Node.data == "fname":
        El = Node.children[0]
        return Dispatch(El, Env)
    if Node.data == "params":
        return [Dispatch(El, Env)
            for El in Node.children]
    if Node.data == "while":
        Env = While(Env)
        Cond, Do = Node.children
        Env.Cond = Dispatch(Cond, Env)
        Env.Body = Dispatch(Do, Env)
        return Env
    if Node.data == "if":
        Env = If(Env)
        Cond, Do, *Else = Node.children
        Env.Cond = Dispatch(Cond, Env)
        Env.Body = Dispatch(Do, Env)
        if Else:
            Env.Other = Dispatch(Else[0], Env)
        return Env
    if Node.data == "block":
        A =  [Dispatch(El, Env) for El in Node.children]
        return  A
    if Node.data == "stmnt":
        return [Dispatch(El, Env) for
            El in Node.children]
    if Node.data == "expr":
        Array = [Dispatch(El, Env) for El in Node.children]
        return Array if len(Array) > 1 else Array[0]
    if Node.data == "quote":
        return tuple([Dispatch(Child, Env)
            for Child in Node.children])
    if Node.data == "symbol":
        Child = Node.children[0]
        return Symbol(Child.value)
    if Node.data == "string":
        return eval(Node.children[0])
    if Node.data == "integer":
        Child = Node.children[0]
        return int(Child.value)
    print("Missing AST:", Node.data)

pp = Parse('''
$def fib (n) {
  $if (= n 1) {
    ret! 0
  }
  $if (= n 2) {
    ret! 1
  }
  (+ (fib (- n 1)) (fib (- n 2)))
}
  
$def main () {
  puts (fib 10)
}
''')

#print(pp.pretty())
Program = Dispatch(pp)
Globals['main'].Call()
