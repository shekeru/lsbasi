{-# LANGUAGE PartialTypeSignatures, BlockArguments #-}
module Tests where

import Parsers
import Text.Parsec (parse)
import Text.Parser.Token
import AST

-- run :: String -> Either _ Block
run = parse (runUnlined $Unlined $ block) ""
pp x v = putStrLn $("Test " <> show x <> " -> ") <> v
check x str valid = pp x case run str of
  Right val -> if val == valid then "{OKAY}" else show val
  Left err -> show err

tests = do
  check 1 "show \"Hello World\"" [Expression [Symbol "show", Literal (String "Hello World")]]
  check 2 "b >> a, *b = 3" [Binding (Variable "b") (Partial (Expression [Symbol "a"])),Binding (Reference (Variable "b")) (Strict (Expression [Literal (Integer 3)]))]
