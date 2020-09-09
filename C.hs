{-# LANGUAGE PartialTypeSignatures #-}

import Text.Parsec hiding (State)
import Text.Parsec.String
import Data.Maybe

fn :: Char -> t -> Parser t
fn ch op = char ch >> pure op

gen :: Parser Double -> [Parser _] -> Parser Double
gen sub set = do
  left <- skipMany space *> sub
  option left $try$ do
    op <- skipMany space *> choice set
    right <- skipMany space *> sub
    pure $ op left right

expr :: Parser Double
expr = gen term [fn '+' (+), fn '-' (-)]

term :: Parser Double
term = gen factor [fn '*' (*), fn '/' (/)]

factor :: Parser Double
factor = do
  value <- optionMaybe $try$ between (char '(') (char ')') expr
  case value of Just v -> pure v; Nothing -> number

number :: Parser Double
number = do
  num <- skipMany space *> many1 digit
  dec <- option "" $ do
    delim <- char '.'
    decimal <- many1 digit
    pure $ delim : decimal
  pure $ read (num <> dec)

main :: IO ()
main = do
  line <- putStr "scalc> " >> getLine
  case parse expr "" line of
    Left err -> print err
    Right xs -> print xs
  main
