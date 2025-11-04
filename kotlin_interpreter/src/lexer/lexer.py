"""
Lexer implementation for Kotlin interpreter.

The Lexer performs lexical analysis (tokenization) of Kotlin source code.
It reads the source character by character and produces a stream of tokens.
"""

from typing import List, Optional
from .token import Token, TokenType, SourceLocation, KEYWORDS


class LexerError(Exception):
    """Exception raised for lexical errors."""
    def __init__(self, message: str, location: SourceLocation):
        self.message = message
        self.location = location
        super().__init__(f"{location}: {message}")


class Lexer:
    """
    Lexical analyzer for Kotlin subset.
    
    Converts source code string into a list of tokens.
    Tracks line and column numbers for error reporting.
    """
    
    def __init__(self, source: str, filename: Optional[str] = None):
        """
        Initialize lexer with source code.
        
        Args:
            source: Kotlin source code as string
            filename: Optional filename for error reporting
        """
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    @property
    def current_char(self) -> Optional[str]:
        """Get current character, or None if at end."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    @property
    def current_location(self) -> SourceLocation:
        """Get current source location."""
        return SourceLocation(self.line, self.column, self.filename)
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Peek ahead at character without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """
        Consume and return current character, update position.
        
        Returns:
            Current character before advancing, or None if at end
        """
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters (except newlines)."""
        while self.current_char and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comment starting with //"""
        if self.current_char == '/' and self.peek() == '/':
            # Skip until end of line
            while self.current_char and self.current_char != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read integer literal."""
        location = self.current_location
        num_str = ''
        
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        
        return Token(TokenType.INT_LITERAL, int(num_str), location)
    
    def read_string(self) -> Token:
        """Read string literal enclosed in double quotes."""
        location = self.current_location
        self.advance()  # Skip opening quote
        
        string_value = ''
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                # Handle escape sequences
                self.advance()
                if self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                elif self.current_char == '\\':
                    string_value += '\\'
                elif self.current_char == '"':
                    string_value += '"'
                elif self.current_char == '$':
                    string_value += '$'
                else:
                    raise LexerError(
                        f"Invalid escape sequence: \\{self.current_char}",
                        self.current_location
                    )
                self.advance()
            elif self.current_char == '\n':
                raise LexerError("Unterminated string literal", location)
            else:
                string_value += self.current_char
                self.advance()
        
        if not self.current_char:
            raise LexerError("Unterminated string literal", location)
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING_LITERAL, string_value, location)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword."""
        location = self.current_location
        identifier = ''
        
        # First character must be letter or underscore
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        # For boolean literals, store Python bool values
        if token_type == TokenType.TRUE:
            return Token(token_type, True, location)
        elif token_type == TokenType.FALSE:
            return Token(token_type, False, location)
        
        return Token(token_type, identifier, location)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens including EOF token at end
            
        Raises:
            LexerError: If invalid syntax is encountered
        """
        self.tokens = []
        
        while self.current_char:
            # Skip whitespace (except newlines)
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Newlines (Kotlin allows statement continuation)
            if self.current_char == '\n':
                location = self.current_location
                self.advance()
                # We'll skip newlines for simplicity in this implementation
                # In full Kotlin, newlines can be significant
                continue
            
            # Numbers
            if self.current_char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            location = self.current_location
            char = self.current_char
            next_char = self.peek()
            
            # ==
            if char == '=' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', location))
                continue
            
            # !=
            if char == '!' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', location))
                continue
            
            # <=
            if char == '<' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', location))
                continue
            
            # >=
            if char == '>' and next_char == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', location))
                continue
            
            # &&
            if char == '&' and next_char == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', location))
                continue
            
            # ||
            if char == '|' and next_char == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', location))
                continue
            
            # ->
            if char == '-' and next_char == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', location))
                continue
            
            # Single-character tokens
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '!': TokenType.NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
                '$': TokenType.DOLLAR,
            }
            
            if char in single_char_tokens:
                token_type = single_char_tokens[char]
                self.tokens.append(Token(token_type, char, location))
                self.advance()
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: '{char}'", location)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.current_location))
        return self.tokens
    
    def __repr__(self) -> str:
        return f"Lexer(pos={self.pos}, line={self.line}, column={self.column})"
