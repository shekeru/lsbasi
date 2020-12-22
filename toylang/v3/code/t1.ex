show "hello world"
print = fn x -> show x end
print "what now"
# show (a = 42) b
fib =
  fn 0 -> 0
  elfn 1 -> 1
  elfn x -> add (fib (add x -1)) (fib (add x -2))
end
print (fib 10)
