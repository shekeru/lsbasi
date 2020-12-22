show "hello world"
also_print = print = fn *xs -> show *xs end
wtf = res = print = fn x -> show x end "owo, wats dis"
print "what now"
also_print "first string" wtf (x = y = 42)
show x y
fib =
  fn 0 -> 0
  elfn 1 -> 1
  elfn x -> add (fib (add x -1)) (fib (add x -2))
end
show (fib 10)
