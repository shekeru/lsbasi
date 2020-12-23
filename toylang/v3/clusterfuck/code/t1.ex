show "hello world"
aprint = print = fn *xs -> show *xs end
wtf = res = print = fn x -> show x end "owo, wats dis"
print "what now"
aprint "first string" wtf (x = y = 42)
show x y
fib =
  fn 0 -> 0
  elfn 1 -> 1
  elfn x -> add (fib (add x -1)) (fib (add x -2))
end
show (fib 10)
# k = [aprint 5]
# [aprint "this"] "that" "too"
