"""
Unit tests for the Lexer.

Tests tokenization of various Kotlin constructs.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from lexer import Lexer, LexerError, Token, TokenType, SourceLocation


class TestLexerBasics:
    """Test basic lexer functionality."""
    
    def test_empty_source(self):
        """Test lexing empty source."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_single_identifier(self):
        """Test lexing a single identifier."""
        lexer = Lexer("hello")
        tokens = lexer.tokenize()
        assert len(tokens) == 2  # identifier + EOF
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "hello"
        assert tokens[1].type == TokenType.EOF
    
    def test_keywords(self):
        """Test lexing keywords."""
        source = "fun val var if else while return"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            TokenType.FUN,
            TokenType.VAL,
            TokenType.VAR,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.WHILE,
            TokenType.RETURN,
            TokenType.EOF
        ]
        
        assert len(tokens) == len(expected)
        for token, expected_type in zip(tokens, expected):
            assert token.type == expected_type


class TestLexerLiterals:
    """Test lexing of literals."""
    
    def test_integer_literals(self):
        """Test lexing integer literals."""
        lexer = Lexer("0 1 42 999")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.INT_LITERAL
        assert tokens[0].value == 0
        assert tokens[1].type == TokenType.INT_LITERAL
        assert tokens[1].value == 1
        assert tokens[2].type == TokenType.INT_LITERAL
        assert tokens[2].value == 42
        assert tokens[3].type == TokenType.INT_LITERAL
        assert tokens[3].value == 999
    
    def test_string_literals(self):
        """Test lexing string literals."""
        lexer = Lexer('"hello" "world"')
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING_LITERAL
        assert tokens[0].value == "hello"
        assert tokens[1].type == TokenType.STRING_LITERAL
        assert tokens[1].value == "world"
    
    def test_string_escape_sequences(self):
        """Test lexing strings with escape sequences."""
        lexer = Lexer(r'"hello\nworld\t!"')
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING_LITERAL
        assert tokens[0].value == "hello\nworld\t!"
    
    def test_boolean_literals(self):
        """Test lexing boolean literals."""
        lexer = Lexer("true false")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.TRUE
        assert tokens[0].value is True
        assert tokens[1].type == TokenType.FALSE
        assert tokens[1].value is False


class TestLexerOperators:
    """Test lexing of operators."""
    
    def test_arithmetic_operators(self):
        """Test lexing arithmetic operators."""
        lexer = Lexer("+ - * / %")
        tokens = lexer.tokenize()
        
        expected = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
        ]
        
        for token, expected_type in zip(tokens[:-1], expected):
            assert token.type == expected_type
    
    def test_comparison_operators(self):
        """Test lexing comparison operators."""
        lexer = Lexer("== != < <= > >=")
        tokens = lexer.tokenize()
        
        expected = [
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_THAN,
            TokenType.GREATER_EQUAL,
        ]
        
        for token, expected_type in zip(tokens[:-1], expected):
            assert token.type == expected_type
    
    def test_logical_operators(self):
        """Test lexing logical operators."""
        lexer = Lexer("&& || !")
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.AND
        assert tokens[1].type == TokenType.OR
        assert tokens[2].type == TokenType.NOT


class TestLexerComplexCode:
    """Test lexing of complete Kotlin code."""
    
    def test_simple_function(self):
        """Test lexing a simple function."""
        source = """
        fun main() {
            val x = 5
            println(x)
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Check key tokens are present
        types = [t.type for t in tokens]
        assert TokenType.FUN in types
        assert TokenType.IDENTIFIER in types
        assert TokenType.VAL in types
        assert TokenType.INT_LITERAL in types
    
    def test_function_with_parameters(self):
        """Test lexing function with parameters."""
        source = "fun add(a: Int, b: Int): Int { return a + b }"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        types = [t.type for t in tokens]
        assert TokenType.FUN in types
        assert TokenType.LPAREN in types
        assert TokenType.RPAREN in types
        assert TokenType.COLON in types
        assert TokenType.INT_TYPE in types
        assert TokenType.RETURN in types
    
    def test_if_statement(self):
        """Test lexing if statement."""
        source = """
        if (x > 0) {
            println("positive")
        } else {
            println("negative")
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        types = [t.type for t in tokens]
        assert TokenType.IF in types
        assert TokenType.ELSE in types
        assert TokenType.GREATER_THAN in types


class TestLexerLocation:
    """Test source location tracking."""
    
    def test_location_tracking(self):
        """Test that locations are tracked correctly."""
        source = "fun\nmain"
        lexer = Lexer(source, filename="test.kt")
        tokens = lexer.tokenize()
        
        # First token (fun) at line 1, col 1
        assert tokens[0].location.line == 1
        assert tokens[0].location.column == 1
        assert tokens[0].location.filename == "test.kt"
        
        # Second token (main) at line 2, col 1
        assert tokens[1].location.line == 2
        assert tokens[1].location.column == 1


class TestLexerComments:
    """Test comment handling."""
    
    def test_single_line_comment(self):
        """Test that single-line comments are skipped."""
        source = """
        val x = 5  // This is a comment
        val y = 10
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Comments should be ignored
        types = [t.type for t in tokens]
        assert TokenType.VAL in types
        # Count VAL tokens
        val_count = sum(1 for t in tokens if t.type == TokenType.VAL)
        assert val_count == 2


class TestLexerErrors:
    """Test error handling."""
    
    def test_unterminated_string(self):
        """Test error on unterminated string."""
        source = '"hello'
        lexer = Lexer(source)
        
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        assert "Unterminated string" in str(exc_info.value)
    
    def test_invalid_character(self):
        """Test error on invalid character."""
        source = "val x = @"
        lexer = Lexer(source)
        
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        assert "Unexpected character" in str(exc_info.value)


class TestLexerHelloWorld:
    """Test lexing the hello world example."""
    
    def test_hello_world_file(self):
        """Test lexing the hello_world.kt example."""
        source = """fun main() {
    val x = 5
    val y = 10
    println(x + y)
}"""
        lexer = Lexer(source, filename="hello_world.kt")
        tokens = lexer.tokenize()
        
        # Verify key tokens
        types = [t.type for t in tokens]
        
        # Should have: fun, main, (, ), {, val, x, =, 5, val, y, =, 10, 
        #              println, (, x, +, y, ), }
        assert types.count(TokenType.FUN) == 1
        assert types.count(TokenType.IDENTIFIER) >= 3  # main, x, y (and println)
        assert types.count(TokenType.VAL) == 2
        assert types.count(TokenType.INT_LITERAL) == 2
        assert types.count(TokenType.PLUS) == 1
        
        # Verify no errors
        assert tokens[-1].type == TokenType.EOF


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
