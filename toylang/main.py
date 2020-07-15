from stdlib import Globals, Symbol
from syntax import Parse

def Eval(Term, Locals): 
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
    if Op == Symbol('set!'):
        Locals[Term[1]] = Exp[1]
        return Locals[Term[1]]
    if isinstance(Op, While) or isinstance(Op, If):
        return Op.Execute(Locals)
    if isinstance(Op, int):
        return Op
    return Op.Call(*Exp)

class Block:
    def __init__(s):
        s.Body = []
    def Execute(s, Locals):
        V = None
        for Term in s.Body:
            V = Eval(Term, Locals)
        return V

class Function(Block):
    def __init__(s):
        super().__init__()
        s.Params = []
    def Call(s, *Args):
        Locals = dict(zip(s.Params, Args))
        return s.Execute(Locals)

class While(Block):
    def __init__(s):
        super().__init__()
        s.Cond = []
    def Execute(s, Locals):
        while Eval(s.Cond, Locals):
            super().Execute(Locals)

class If(Block):
    def __init__(s):
        super().__init__()
        s.Cond = []
    def Execute(s, Locals):
        if Eval(s.Cond, Locals):
            super().Execute(Locals)

def Dispatch(Node, Env = None):
    if Node.data == "function":
        Env = Function()
        for El in Node.children:
            Dispatch(El, Env)
        return Env
    if Node.data == "fname":
        El = Node.children[0]
        Env.Name = Dispatch(El, Env)
        Globals[Env.Name] = Env
        return Env
    if Node.data == "param":
        Env.Params.append(Dispatch \
            (Node.children[0], Env))
        return
    if Node.data == "while":
        Env = While()
        Cond, *Do = Node.children
        Env.Cond = Dispatch(Cond, Env)
        [Dispatch(El, Env) for El in Do]
        return Env
    if Node.data == "if":
        Env = If()
        Cond, *Do = Node.children
        Env.Cond = Dispatch(Cond, Env)
        [Dispatch(El, Env) for El in Do]
        return Env
    if Node.data == "block":
        for El in Node.children:
            Env.Body.append(Dispatch(El, Env))
        return
    if Node.data == "stmnt":
        return [Dispatch(El, Env) for
            El in Node.children]
    if Node.data == "expr":
        Array = []
        for Child in Node.children:
            Array.append(Dispatch(Child, Env))
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
$def pe1 (x y) {
  set! sum 0
  $while (< x y) {
    set! mod (* (% x 5) (% x 3))
    $if (~ mod) {
      set! sum (+ sum x)
    }
    set! x (+ x 1)
  }
  sum
}
  
$def main () {
  puts (pe1 1 1000)
}

''')

#print(pp.pretty())
[*map(Dispatch, pp.children)]
Globals['main'].Call()
