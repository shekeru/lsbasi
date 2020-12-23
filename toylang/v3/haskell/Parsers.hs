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
import Debug.Trace
import AST

block :: Parser Block
block = sepEndBy expr $_NL <|> some (chew $char ',')

reduceExpr :: Expr -> Expr
reduceExpr (Expression [x@(Expression _)]) = reduceExpr x
reduceExpr xs = xs

expr :: Parser Expr
expr = reduceExpr <$> do
  try (bind)
  <|> (symbol "_" >> pure TrapValue)
  <|> Expression <$> (try.parens.some.token) expr
  <|> Expression <$> flip sepEndBy1 (char ' ')
    (try (Literal <$> literal <|> Symbol <$> label))

fnFull :: Parser Expr
fnFull = do
  chew (symbol "fn") <* _NL
  args <- sepEndBy arg (char ' ') <* _NL
  parts <- some fnPart
  _NL *> chew (symbol ";;")
  pure $Function args parts

fnPart :: Parser FnCase
fnPart = do
  _NL *> chew (symbol "::")
  def <- optional (chew $symbol "else")
  args <- case def of
    Nothing -> Just <$> try block
    Just _ -> pure Nothing
  chew (symbol "->")
  FnGuard args <$> block

arg :: Parser Args
arg = do
  ref <- optional (char '*')
  case ref of
    Just _ -> VarArgs <$> label
    Nothing -> Arg <$> label

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
literal = try do
  (symbol "nil" <|> symbol "()" >> pure Nil)
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

chew :: Parser a -> Parser a
chew x = try spaces *> x <* try spaces
_NL = many newline
