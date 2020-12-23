# Everything is an Expression
foo >> (show "Hello World")
# Lazy Assignment, b Always Evaluates to a
# Also Assign to A lol with *
a = 0, b >> a, *b = 10, c >> b
show a b c, *c = 30, show a b c
foo foo
