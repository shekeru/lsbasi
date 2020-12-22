from lark import Lark, Token, Tree

syntax = Lark(r"""
    start: _NL* stmnt*
    block: (("->" _NL*) | _NL+) stmnt*
    assign: symbol _NL* "=" _NL* stmnt
    stmnt: (assign | fn | if | strict | partial) _NL*
    fn: "fn" _NL* symbol* block "end"
    if: "if" _NL* stmnt block elif* else? "end"
    elif: "elif" _NL* stmnt block
    else: "else" _NL* stmnt block
    partial: "[" expr* "]"
    expr: string | integer | symbol
    strict: (expr+ _NL) | "(" expr* ")" | expr+ "->" | expr
    symbol: /(?!([~;\(\[=]|if|->|end))\S+(?<![\)\]])/
    string: ESCAPED_STRING
    integer: SIGNED_INT
    %import common.NEWLINE -> _NL
    %import common.SIGNED_INT
    %import common.ESCAPED_STRING
    %import common.WS_INLINE
    COMMENT: ";" /[^\n]/*
    %ignore WS_INLINE
    %ignore COMMENT
""", parser="earley")

def Parse(txt):
    return syntax.parse(open("Code/"+txt).read())

#print(Parse("t1.ex").pretty())
