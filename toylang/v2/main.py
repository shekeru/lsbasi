from syntax import Parse
from structs import *            

def Dispatch(Node, Env = None):
    if Node.data == "start":
        Env = Program(Globals)
        for El in Node.children:
            Dispatch(El, Env)
        return Env
    if Node.data == "function":
        Env = Function(Env)
        Name, Params, Body = Node.children
        Env.Name = Dispatch(Name, Env)
        Env.Params = Dispatch(Params, Env)
        Env.Body = Dispatch(Body, Env)
        Env.Parent[Env.Name] = Env
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
        return [Dispatch(El, Env) for El in Node.children]
    if Node.data == "stmnt":
        return [Dispatch(El, Env) for El in Node.children]
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
  $while (< x 10) {
    fizzb x
    set! x (+ x 1)
  }
}
''')

#print(pp.pretty())
Script = Dispatch(pp)
Script['main'].Call()
