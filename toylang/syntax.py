from lark import Lark, Token, Tree

syntax = Lark(r"""
    start: _NL* (function)*
    function: "$def" fname "(" param* ")" _NL body* _NL*
    param: symbol
    fname: symbol
    body: expr+ _NL
    expr: string | integer | symbol | quote | "(" expr* ")"
    quote: "'(" expr* ")"
    symbol: /[^()\s'"$]+/
    string: ESCAPED_STRING
    integer: SIGNED_INT
    %import common.NEWLINE -> _NL
    %import common.SIGNED_INT
    %import common.ESCAPED_STRING
    %import common.WS_INLINE
    %ignore WS_INLINE
    COMMENT: "#" /[^\n]/*
    %ignore COMMENT
""", parser="earley")

def Parse(txt):
    return syntax.parse(txt)

