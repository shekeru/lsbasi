from stdlib import Globals, Symbol
from syntax import Parse

class Function:
    def __init__(s):
        s.Params = []
        s.Body = []
    def Call(s, *Args):
        Locals = dict(zip(s.Params, Args))
        for Term in s.Body:
            V = Execute(Term, Locals)
        return V

def Execute(Term, Locals):
    Array = []
    for Ref in Term:
        if isinstance(Ref, list):
            Array.append(Execute(Ref, Locals))
        else:
            Array.append(Locals[Ref] \
                if Ref in Locals else Ref)
    Op, *Exp = Array
    if Op in Globals:
        return Globals[Op].Call(*Exp)
    print("Failed", Array)

def Dispatch(Node, Fn = None):
    if Node.data == "function":
        Fn = Function()
        for El in Node.children:
            Dispatch(El, Fn)
    if Node.data == "fname":
        El = Node.children[0]
        Fn.Name = Dispatch(El, Fn)
        Globals[Fn.Name] = Fn
    if Node.data == "param":
        El = Node.children[0]
        Fn.Params.append(Dispatch(El, Fn))
    if Node.data == "body":
        Fn.Body.append([Dispatch(El, Fn)
            for El in Node.children])
    if Node.data == "expr":
        Array = []
        for Child in Node.children:
            Array.append(Dispatch(Child, Fn))
        return Array if len(Array) > 1 else Array[0]
    if Node.data == "quote":
        return tuple([Dispatch(Child, Fn)
            for Child in Node.children])
    if Node.data == "symbol":
        Child = Node.children[0]
        return Symbol(Child.value)
    if Node.data == "string":
        return eval(Node.children[0])
    if Node.data == "integer":
        Child = Node.children[0]
        return int(Child.value)

pp = Parse('''
$def sq (x)
  * x x

$def test (x)
  puts x
  
$def main ()
  test "hello world"
  puts "5*5:" (sq 5)
  puts '(1 2 3)
 
''')

[*map(Dispatch, pp.children)]
Globals['main'].Call()
