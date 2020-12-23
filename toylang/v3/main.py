import Parser
# Data Structure
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
# Function Calls

# Evaluate Line
def Eval(Node, Env):

    print("unknown token", Node)
# Prelude, Globals
Globals, V = EnvS(), None
def Std_Puts(*xs):
    print(*xs)
    return xs if len(xs) > 1 else xs[0]
Globals[Parser.Symbol('show')] = Std_Puts
# Run Program
Lines = Parser.ReadAST("s1")
for Stmnt in Lines:
    V = Eval(Stmnt, Globals)
print(">>>", V)
