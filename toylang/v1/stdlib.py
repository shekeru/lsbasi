Globals = {}

class Puts:
    def Call(s, *Args):
        return print(*Args)
Globals["puts"] = Puts()

class Add:
    def Call(s, *Args):
        return sum(Args)
Globals["+"] = Add()

class Mul:
    def Call(s, *Args):
        V = 1
        for x in Args:
            V *= x
        return V
Globals["*"] = Mul()

class Sub:
    def Call(s, *Args):
        V = Args[0]
        for x in Args[1:]:
            V -= x
        return V
Globals["-"] = Sub()

class LT:
    def Call(s, A, B):
        return A < B
Globals["<"] = LT()

class EQ:
    def Call(s, A, B):
        return A == B
Globals["="] = EQ()

class Mod:
    def Call(s, A, B):
        return A % B
Globals["%"] = Mod()

class Not:
    def Call(s, A):
        return not A
Globals["~"] = Not()

class Symbol(str):
    def __repr__(s):
        return f'Symbol({eval(super().__repr__())})'
    def __str__(s):
        return repr(s)
