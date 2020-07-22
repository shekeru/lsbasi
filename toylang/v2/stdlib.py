from structs import Block
Globals = {}

class Puts(Block):
    def Call(s, *Args, **KW):
        return print(*Args)
Globals["puts"] = Puts()

class Add(Block):
    def Call(s, *Args, **KW):
        return sum(Args)
Globals["+"] = Add()

class Mul(Block):
    def Call(s, *Args, **KW):
        V = 1
        for x in Args:
            V *= x
        return V
Globals["*"] = Mul()

class Sub(Block):
    def Call(s, *Args, **KW):
        V = Args[0]
        for x in Args[1:]:
            V -= x
        return V
Globals["-"] = Sub()

class LT(Block):
    def Call(s, A, B, **KW):
        return A < B
Globals["<"] = LT()

class EQ(Block):
    def Call(s, A, B, **KW):
        return A == B
Globals["="] = EQ()

class Mod(Block):
    def Call(s, A, B, **KW):
        return A % B
Globals["%"] = Mod()

class Not(Block):
    def Call(s, A, **KW):
        return not A
Globals["~"] = Not()
