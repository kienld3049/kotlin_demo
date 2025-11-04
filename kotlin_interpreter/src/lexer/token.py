"""
Token definitions for Kotlin lexer.

This module defines:
- TokenType enum: All token types in our Kotlin subset
- SourceLocation: Track token positions in source code
- Token: Represents a lexical token with type, value, and location
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """Token types for Kotlin subset."""
    
    # Keywords
    FUN = auto()
    VAL = auto()
    VAR = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Types
    INT_TYPE = auto()      # Int
    STRING_TYPE = auto()   # String
    BOOLEAN_TYPE = auto()  # Boolean
    UNIT_TYPE = auto()     # Unit
    
    # Literals
    INT_LITERAL = auto()
    STRING_LITERAL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    
    # Comparison
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    LESS_THAN = auto()     # <
    LESS_EQUAL = auto()    # <=
    GREATER_THAN = auto()  # >
    GREATER_EQUAL = auto() # >=
    
    # Logical
    AND = auto()           # &&
    OR = auto()            # ||
    NOT = auto()           # !
    
    # Assignment
    ASSIGN = auto()        # =
    
    # Delimiters
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    COMMA = auto()         # ,
    COLON = auto()         # :
    SEMICOLON = auto()     # ;
    ARROW = auto()         # ->
    DOLLAR = auto()        # $ (for string templates)
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    
    def __repr__(self) -> str:
        return f"TokenType.{self.name}"


@dataclass(frozen=True)
class SourceLocation:
    """Represents a location in source code."""
    line: int
    column: int
    filename: Optional[str] = None
    
    def __str__(self) -> str:
        if self.filename:
            return f"{self.filename}:{self.line}:{self.column}"
        return f"{self.line}:{self.column}"
    
    def __repr__(self) -> str:
        return f"SourceLocation(line={self.line}, column={self.column})"


@dataclass
class Token:
    """Represents a lexical token."""
    type: TokenType
    value: Any
    location: SourceLocation
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, {self.location})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def is_keyword(self) -> bool:
        """Check if token is a keyword."""
        return self.type in {
            TokenType.FUN, TokenType.VAL, TokenType.VAR,
            TokenType.IF, TokenType.ELSE, TokenType.WHILE,
            TokenType.RETURN, TokenType.TRUE, TokenType.FALSE
        }
    
    @property
    def is_type(self) -> bool:
        """Check if token is a type keyword."""
        return self.type in {
            TokenType.INT_TYPE, TokenType.STRING_TYPE,
            TokenType.BOOLEAN_TYPE, TokenType.UNIT_TYPE
        }
    
    @property
    def is_literal(self) -> bool:
        """Check if token is a literal."""
        return self.type in {
            TokenType.INT_LITERAL, TokenType.STRING_LITERAL,
            TokenType.TRUE, TokenType.FALSE
        }
    
    @property
    def is_operator(self) -> bool:
        """Check if token is an operator."""
        return self.type in {
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
            TokenType.DIVIDE, TokenType.MODULO,
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS_THAN, TokenType.LESS_EQUAL,
            TokenType.GREATER_THAN, TokenType.GREATER_EQUAL,
            TokenType.AND, TokenType.OR, TokenType.NOT
        }


# Keyword mapping for lexer
KEYWORDS = {
    'fun': TokenType.FUN,
    'val': TokenType.VAL,
    'var': TokenType.VAR,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'Int': TokenType.INT_TYPE,
    'String': TokenType.STRING_TYPE,
    'Boolean': TokenType.BOOLEAN_TYPE,
    'Unit': TokenType.UNIT_TYPE,
}
