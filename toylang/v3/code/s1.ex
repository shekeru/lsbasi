# Everything is an Expression
show "Hello World"
# Lazy Assignment, b Always Evaluates to a
# Also Assign to A lol with *
b >> a, *b = 3
# Functions, Require Lazy Assignment to be bound
print >> fn *xs -> show xs;;
# Guarded Functions
fib >> fn x y
  :: 0, y -> 0
  :: x, 1 -> 1
  :: else ->
    add (fib (add x -1)) (fib (add x -2))
;;
# If/Cond, Expr = True
var = do
  :: fib 10 /=/ 55 ->
    "never happens"
  :: fib 0 == 0 ->
    "should happen"
  :: else ->
    "default"
;;
# Case, Expr == x
snd = case x
  :: 0 -> 1
  :: 1 -> 1
  :: else -> x
;;
# If, (Expr x) = True
bleh = if x
  :: checkfn ->
  :: otherfn ->
  :: else ->
;;
# ---- Phase 2
# Math Operators
v = 5 + 2 - 3 / 3 % 9 // 7
# Boolean Operators
v = (k == a) && (a /=/ b) || (!! b)
# Comparison Operators
v = a <= v <= x >= y =< x
# Objects

# Updates Array Value, Instead Array
ref >> Array[Lol][Lol][LOl]
*ref = 3
# Assignment Blocks, Lazy (->>) / Strict (=>)
ref (=>) (->>) (= ->) (>> ->)
  operation 1
  operation 2
;;
