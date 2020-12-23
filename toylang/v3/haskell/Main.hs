{-# LANGUAGE PartialTypeSignatures, BlockArguments #-}
module Main where

import Parsers
import Tests
import AST

main :: IO ()
main = do
  tests
