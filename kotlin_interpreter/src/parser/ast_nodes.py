"""
Abstract Syntax Tree (AST) node definitions for Kotlin interpreter.

This module defines all AST node types representing Kotlin constructs.
Each node represents a syntactic element in the parsed program.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod

from ..lexer.token import SourceLocation


# Base classes

class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def __repr__(self) -> str:
        """String representation for debugging."""
        pass


@dataclass
class Expression(ASTNode):
    """Base class for expressions (produce values)."""
    location: SourceLocation


@dataclass
class Statement(ASTNode):
    """Base class for statements (perform actions)."""
    location: SourceLocation


@dataclass
class Declaration(ASTNode):
    """Base class for declarations."""
    location: SourceLocation


# Program structure

@dataclass
class Program(ASTNode):
    """Root node representing entire program."""
    declarations: List[Declaration]
    
    def __repr__(self) -> str:
        return f"Program({len(self.declarations)} declarations)"


# Declarations

@dataclass
class FunctionDeclaration(Declaration):
    """Function declaration: fun name(params): returnType { body }"""
    name: str
    parameters: List['Parameter']
    return_type: Optional[str]  # None means Unit (inferred)
    body: 'BlockStatement'
    location: SourceLocation
    
    def __repr__(self) -> str:
        params = ', '.join(str(p) for p in self.parameters)
        ret_type = f": {self.return_type}" if self.return_type else ""
        return f"FunctionDeclaration({self.name}({params}){ret_type})"


@dataclass
class Parameter:
    """Function parameter: name: type"""
    name: str
    type: str
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.type}"


@dataclass
class VariableDeclaration(Declaration):
    """Variable declaration: val/var name: type? = initializer?"""
    is_mutable: bool  # True for var, False for val
    name: str
    type: Optional[str]  # None means type inference
    initializer: Optional[Expression]
    location: SourceLocation
    
    def __repr__(self) -> str:
        mut = "var" if self.is_mutable else "val"
        type_str = f": {self.type}" if self.type else ""
        init_str = f" = {self.initializer}" if self.initializer else ""
        return f"{mut} {self.name}{type_str}{init_str}"


# Statements

@dataclass
class BlockStatement(Statement):
    """Block of statements: { statement1; statement2; ... }"""
    statements: List[Statement]
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Block({len(self.statements)} statements)"


@dataclass
class ExpressionStatement(Statement):
    """Statement that is just an expression."""
    expression: Expression
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"ExpressionStatement({self.expression})"


@dataclass
class IfStatement(Statement):
    """If statement: if (condition) thenBranch else elseBranch?"""
    condition: Expression
    then_branch: Statement
    else_branch: Optional[Statement]
    location: SourceLocation
    
    def __repr__(self) -> str:
        else_str = " else ..." if self.else_branch else ""
        return f"If({self.condition}){else_str}"


@dataclass
class WhileStatement(Statement):
    """While loop: while (condition) body"""
    condition: Expression
    body: Statement
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"While({self.condition})"


@dataclass
class ReturnStatement(Statement):
    """Return statement: return expression?"""
    value: Optional[Expression]
    location: SourceLocation
    
    def __repr__(self) -> str:
        val_str = str(self.value) if self.value else "Unit"
        return f"Return({val_str})"


@dataclass
class DeclarationStatement(Statement):
    """Declaration as statement (for local variables in function bodies)."""
    declaration: Declaration
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"DeclStmt({self.declaration})"


# Expressions

@dataclass
class LiteralExpression(Expression):
    """Literal value: 42, "hello", true"""
    value: Any  # int, str, bool
    literal_type: str  # "Int", "String", "Boolean"
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Literal({self.literal_type}: {repr(self.value)})"


@dataclass
class IdentifierExpression(Expression):
    """Variable reference: variableName"""
    name: str
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Identifier({self.name})"


@dataclass
class BinaryExpression(Expression):
    """Binary operation: left operator right"""
    left: Expression
    operator: str  # +, -, *, /, %, ==, !=, <, <=, >, >=, &&, ||
    right: Expression
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Binary({self.left} {self.operator} {self.right})"


@dataclass
class UnaryExpression(Expression):
    """Unary operation: operator operand"""
    operator: str  # -, !
    operand: Expression
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Unary({self.operator}{self.operand})"


@dataclass
class CallExpression(Expression):
    """Function call: functionName(arguments)"""
    function_name: str
    arguments: List[Expression]
    location: SourceLocation
    
    def __repr__(self) -> str:
        args = ', '.join(str(arg) for arg in self.arguments)
        return f"Call({self.function_name}({args}))"


@dataclass
class AssignmentExpression(Expression):
    """Assignment: target = value"""
    target: str  # Variable name
    value: Expression
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"Assign({self.target} = {self.value})"


@dataclass
class IfExpression(Expression):
    """If expression: if (condition) thenExpr else elseExpr"""
    condition: Expression
    then_branch: Expression
    else_branch: Expression  # Required in expression form
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"IfExpr({self.condition} ? {self.then_branch} : {self.else_branch})"


@dataclass
class StringTemplateExpression(Expression):
    """String template: "text $variable more text" """
    parts: List[Expression]  # Mix of LiteralExpression and other expressions
    location: SourceLocation
    
    def __repr__(self) -> str:
        return f"StringTemplate({len(self.parts)} parts)"


# Helper functions for AST construction

def get_node_location(node: ASTNode) -> SourceLocation:
    """Get source location from any AST node."""
    if hasattr(node, 'location'):
        return node.location
    raise AttributeError(f"Node {type(node).__name__} has no location attribute")


def is_expression(node: ASTNode) -> bool:
    """Check if node is an expression."""
    return isinstance(node, Expression)


def is_statement(node: ASTNode) -> bool:
    """Check if node is a statement."""
    return isinstance(node, Statement)


def is_declaration(node: ASTNode) -> bool:
    """Check if node is a declaration."""
    return isinstance(node, Declaration)
