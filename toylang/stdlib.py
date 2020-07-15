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

class Symbol(str):
    def __repr__(s):
        return f'Symbol({eval(super().__repr__())})'
    def __str__(s):
        return repr(s)
