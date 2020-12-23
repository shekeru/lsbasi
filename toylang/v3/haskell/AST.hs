module AST where

data Args =
    Arg String |
    VarArgs String
  deriving (Show, Eq)
type Block = [Expr]

data FnCase = FnGuard (Maybe [Expr]) Block
  deriving (Show, Eq)
data Case = Guard (Maybe Expr) Block
  deriving (Show, Eq)

data LVal =
    Variable String |
    Reference LVal
  deriving (Show, Eq)

data RVal =
    Strict Expr |
    Partial Expr
  deriving (Show, Eq)

data Expr =
    Symbol String |
    Expression [Expr] |
    Binding LVal RVal |
    Function [Args] [FnCase] |
    Conditional [Case] |
    CaseStruct [Case] |
    PipeStruct [Case] |
    Literal Types |
    TrapValue
  deriving (Show, Eq)

data Types = Nil |
    Float Double |
    Integer Integer |
    Character Char |
    String String |
    Boolean Bool
  deriving (Show, Eq)
