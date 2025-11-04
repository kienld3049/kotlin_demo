"""
Recursive Descent Parser for Kotlin interpreter.

Converts token stream into Abstract Syntax Tree (AST).
Implements grammar rules for Kotlin subset.
"""

from typing import List, Optional
from ..lexer.token import Token, TokenType
from .ast_nodes import *


class ParseError(Exception):
    """Exception raised for parsing errors."""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"{token.location}: {message}")


class Parser:
    """
    Recursive descent parser for Kotlin subset.
    
    Grammar (simplified):
        program         → declaration* EOF
        declaration     → funDecl | varDecl
        funDecl         → "fun" IDENTIFIER "(" parameters? ")" (":" type)? block
        varDecl         → ("val" | "var") IDENTIFIER (":" type)? ("=" expression)?
        
        statement       → exprStmt | ifStmt | whileStmt | returnStmt | block
        block           → "{" statement* "}"
        exprStmt        → expression
        ifStmt          → "if" "(" expression ")" statement ("else" statement)?
        whileStmt       → "while" "(" expression ")" statement
        returnStmt      → "return" expression?
        
        expression      → assignment
        assignment      → IDENTIFIER "=" assignment | logicalOr
        logicalOr       → logicalAnd ("||" logicalAnd)*
        logicalAnd      → equality ("&&" equality)*
        equality        → comparison (("==" | "!=") comparison)*
        comparison      → addition (("<" | "<=" | ">" | ">=") addition)*
        addition        → multiplication (("+" | "-") multiplication)*
        multiplication  → unary (("*" | "/" | "%") unary)*
        unary           → ("!" | "-") unary | call
        call            → primary ("(" arguments? ")")?
        primary         → literal | IDENTIFIER | "(" expression ")" | ifExpr
        ifExpr          → "if" "(" expression ")" expression "else" expression
    """
    
    def __init__(self, tokens: List[Token]):
        """Initialize parser with token list."""
        self.tokens = tokens
        self.current = 0
    
    # Token management
    
    @property
    def is_at_end(self) -> bool:
        """Check if we've reached end of tokens."""
        return self.peek().type == TokenType.EOF
    
    def peek(self, offset: int = 0) -> Token:
        """Look at token without consuming it."""
        pos = self.current + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[pos]
    
    def previous(self) -> Token:
        """Get previously consumed token."""
        return self.tokens[self.current - 1]
    
    def advance(self) -> Token:
        """Consume and return current token."""
        if not self.is_at_end:
            self.current += 1
        return self.previous()
    
    def check(self, token_type: TokenType) -> bool:
        """Check if current token matches type without consuming."""
        if self.is_at_end:
            return False
        return self.peek().type == token_type
    
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any type, consume if match."""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error."""
        if self.check(token_type):
            return self.advance()
        raise ParseError(message, self.peek())
    
    # Parsing methods
    
    def parse(self) -> Program:
        """Parse entire program."""
        declarations = []
        while not self.is_at_end:
            declarations.append(self.declaration())
        return Program(declarations)
    
    def declaration(self) -> Declaration:
        """Parse a declaration (function or variable)."""
        try:
            if self.match(TokenType.FUN):
                return self.function_declaration()
            if self.match(TokenType.VAL, TokenType.VAR):
                return self.variable_declaration()
            
            # If not a declaration, treat as statement in global scope
            # (Not typical in Kotlin but useful for testing)
            raise ParseError("Expected declaration (fun/val/var)", self.peek())
        
        except ParseError:
            # Error recovery: skip to next statement
            self.synchronize()
            raise
    
    def function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration."""
        location = self.previous().location
        
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        
        # Parse parameters
        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(self.parameter())
            while self.match(TokenType.COMMA):
                parameters.append(self.parameter())
        
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        
        # Optional return type
        return_type = None
        if self.match(TokenType.COLON):
            return_type = self.type_annotation()
        
        # Function body - must start with '{'
        self.consume(TokenType.LBRACE, "Expected '{' before function body")
        body = self.block_statement()
        
        # Signature: (location, name, parameters, return_type, body)
        return FunctionDeclaration(location, name, parameters, return_type, body)
    
    def parameter(self) -> Parameter:
        """Parse function parameter: name: type"""
        location = self.peek().location
        name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
        self.consume(TokenType.COLON, "Expected ':' after parameter name")
        param_type = self.type_annotation()
        return Parameter(name, param_type, location)
    
    def type_annotation(self) -> str:
        """Parse type annotation."""
        if self.match(TokenType.INT_TYPE):
            return "Int"
        elif self.match(TokenType.STRING_TYPE):
            return "String"
        elif self.match(TokenType.BOOLEAN_TYPE):
            return "Boolean"
        elif self.match(TokenType.UNIT_TYPE):
            return "Unit"
        else:
            raise ParseError("Expected type annotation", self.peek())
    
    def variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration."""
        is_mutable = self.previous().type == TokenType.VAR
        location = self.previous().location
        
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        # Optional type annotation
        var_type = None
        if self.match(TokenType.COLON):
            var_type = self.type_annotation()
        
        # Optional initializer
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        
        # Correct order: location, is_mutable, name, var_type (Optional), initializer (Optional)
        return VariableDeclaration(location, is_mutable, name, var_type, initializer)
    
    def statement(self) -> Statement:
        """Parse a statement."""
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.LBRACE):
            return self.block_statement()
        if self.match(TokenType.VAL, TokenType.VAR):
            # Variable declaration as statement
            var_decl = self.variable_declaration()
            return DeclarationStatement(var_decl, var_decl.location)
        
        return self.expression_statement()
    
    def block_statement(self) -> BlockStatement:
        """Parse block statement: { ... }"""
        location = self.previous().location
        statements = []
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end:
            statements.append(self.statement())
        
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        return BlockStatement(statements, location)
    
    def if_statement(self) -> IfStatement:
        """Parse if statement."""
        location = self.previous().location
        
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        
        then_branch = self.statement()
        
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        
        return IfStatement(condition, then_branch, else_branch, location)
    
    def while_statement(self) -> WhileStatement:
        """Parse while statement."""
        location = self.previous().location
        
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        
        body = self.statement()
        
        return WhileStatement(condition, body, location)
    
    def return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        location = self.previous().location
        
        value = None
        # If there's an expression, parse it
        if not self.check(TokenType.RBRACE) and not self.is_at_end:
            # Check if next token could start an expression
            if self.peek().type in [
                TokenType.IDENTIFIER, TokenType.INT_LITERAL, TokenType.STRING_LITERAL,
                TokenType.TRUE, TokenType.FALSE, TokenType.LPAREN,
                TokenType.MINUS, TokenType.NOT, TokenType.IF
            ]:
                value = self.expression()
        
        return ReturnStatement(value, location)
    
    def expression_statement(self) -> ExpressionStatement:
        """Parse expression statement."""
        expr = self.expression()
        return ExpressionStatement(expr, expr.location)
    
    # Expression parsing (precedence climbing)
    
    def expression(self) -> Expression:
        """Parse expression."""
        return self.assignment()
    
    def assignment(self) -> Expression:
        """Parse assignment expression."""
        expr = self.logical_or()
        
        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.assignment()
            
            if isinstance(expr, IdentifierExpression):
                return AssignmentExpression(expr.name, value, equals.location)
            
            raise ParseError("Invalid assignment target", equals)
        
        return expr
    
    def logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self.logical_and()
        
        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.logical_and()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self.equality()
        
        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.equality()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def equality(self) -> Expression:
        """Parse equality expression."""
        expr = self.comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def comparison(self) -> Expression:
        """Parse comparison expression."""
        expr = self.addition()
        
        while self.match(
            TokenType.LESS_THAN, TokenType.LESS_EQUAL,
            TokenType.GREATER_THAN, TokenType.GREATER_EQUAL
        ):
            operator = self.previous().value
            right = self.addition()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def addition(self) -> Expression:
        """Parse addition/subtraction expression."""
        expr = self.multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().value
            right = self.multiplication()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def multiplication(self) -> Expression:
        """Parse multiplication/division expression."""
        expr = self.unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryExpression(expr, operator, right, expr.location)
        
        return expr
    
    def unary(self) -> Expression:
        """Parse unary expression."""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous().value
            operand = self.unary()
            return UnaryExpression(operator, operand, self.previous().location)
        
        return self.call()
    
    def call(self) -> Expression:
        """Parse function call."""
        expr = self.primary()
        
        # Check for function call
        if isinstance(expr, IdentifierExpression) and self.match(TokenType.LPAREN):
            return self.finish_call(expr)
        
        return expr
    
    def finish_call(self, callee: IdentifierExpression) -> CallExpression:
        """Finish parsing function call after '('."""
        arguments = []
        
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())
        
        paren = self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        
        return CallExpression(callee.name, arguments, callee.location)
    
    def primary(self) -> Expression:
        """Parse primary expression."""
        # Literals
        if self.match(TokenType.TRUE):
            return LiteralExpression(True, "Boolean", self.previous().location)
        
        if self.match(TokenType.FALSE):
            return LiteralExpression(False, "Boolean", self.previous().location)
        
        if self.match(TokenType.INT_LITERAL):
            token = self.previous()
            return LiteralExpression(token.value, "Int", token.location)
        
        if self.match(TokenType.STRING_LITERAL):
            token = self.previous()
            return LiteralExpression(token.value, "String", token.location)
        
        # Identifier
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            return IdentifierExpression(token.value, token.location)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # If expression
        if self.match(TokenType.IF):
            return self.if_expression()
        
        raise ParseError("Expected expression", self.peek())
    
    def if_expression(self) -> IfExpression:
        """Parse if expression (must have else branch)."""
        location = self.previous().location
        
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        
        then_branch = self.expression()
        
        self.consume(TokenType.ELSE, "If expression requires 'else' branch")
        else_branch = self.expression()
        
        return IfExpression(condition, then_branch, else_branch, location)
    
    def synchronize(self):
        """Synchronize parser after error (error recovery)."""
        self.advance()
        
        while not self.is_at_end:
            # Stop at statement boundaries
            if self.previous().type in [TokenType.SEMICOLON, TokenType.RBRACE]:
                return
            
            if self.peek().type in [
                TokenType.FUN, TokenType.VAL, TokenType.VAR,
                TokenType.IF, TokenType.WHILE, TokenType.RETURN
            ]:
                return
            
            self.advance()
