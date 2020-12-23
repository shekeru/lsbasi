{-# LANGUAGE PartialTypeSignatures, BlockArguments #-}
module Parsers where

import Text.Parsec (parse)
import Control.Applicative
import Text.Parsec.String (Parser)
import Text.Parser.Combinators
import Text.Parser.LookAhead
import Text.Parser.Token
import Text.Parser.Char
import Data.Function
import AST

block :: Parser Block
block = sepEndBy1 expr $some (token $char ',') <|> some newline

reduceExpr :: Expr -> Expr
reduceExpr (Expression [x@(Expression _)]) = reduceExpr x
reduceExpr xs = xs

expr :: Parser Expr
expr = reduceExpr <$> do try (bind)
  <|> (symbol "_" >> pure TrapValue)
  <|> Expression <$> (try.parens.some.token) expr
  <|> Expression <$> flip sepBy1 (char ' ')
    (Literal <$> literal <|> Symbol <$> label)

lval :: Parser LVal
lval = do
  ref <- optional (char '*')
  case ref of
    Just _ -> Reference <$> lval
    Nothing -> Variable <$> label

bind :: Parser Expr
bind = do
  left <- token lval
  op <- (symbol "=" >> pure Strict)
    <|> (symbol ">>" >> pure Partial)
  expr >>= pure.Binding left.op

label :: Parser String
label = some (oneOf validChars)
validChars = ['a'..'z'] <> ['A'..'Z'] <> ['0'..'9']

literal :: Parser Types
literal = (symbol "nil" <|> symbol "()" >> pure Nil)
  <|> Float <$> float
  <|> Integer <$> integer'
  <|> Character <$> charLiteral
  <|> String <$> stringLiteral

float :: Parser Double
float = try do
  plus <- optional $char '+'
  minus <- optional $char '-'
  case minus of
    Just _ -> negate <$> double
    Nothing -> double
