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
    return Op.Call(*Exp)
    print("Missed:", Term, Array)

def Execute(Terms, Locals):
    V = None
    for Term in Terms:
        V = Eval(Term, Locals)
    return V

class Block:
    def __init__(s):
        s.Body = []

class Function(Block):
    def __init__(s):
        super().__init__()
        s.Params = []
    def Call(s, *Args):
        Locals = dict(zip(s.Params, Args))
        return Execute(s.Body, Locals)

class While(Block):
    def __init__(s):
        super().__init__()
        s.Cond = []
    def Handle(s, Locals):
        while Eval(s.Cond, Locals):
            Execute(s.Body, Locals)

class If(Block):
    def __init__(s):
        super().__init__()
        s.Cond = []
        s.Other = []
    def Handle(s, Locals):
        if Eval(s.Cond, Locals):
            Execute(s.Body, Locals)
        else:
            Execute(s.Other, Locals)
            

def Dispatch(Node, Env = None):
    if Node.data == "function":
        Env = Function()
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
        Env = While()
        Cond, Do = Node.children
        Env.Cond = Dispatch(Cond, Env)
        Env.Body = Dispatch(Do, Env)
        return Env
    if Node.data == "if":
        Env = If()
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
$def fizzb (x) {
  set! f3 (% x 3)
  set! f5 (% x 5)
  $if (~ (+ f5 f3)) {
    puts "FizzBuzz"
  }
  $else {
    $if (~ f3) {
      puts "Fizz"
    }
    $if (~ f5) {
      puts "Buzz"
    }
    $if (< 0 (* f5 f3)) {
      puts x
    }
  }
}
  
$def main () {
  set! x 1
  $while (< x 100) {
    fizzb x
    set! x (+ x 1)
  }
}
''')

#print(pp.pretty())
[*map(Dispatch, pp.children)]
Globals['main'].Call()
