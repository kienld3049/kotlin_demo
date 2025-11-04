"""
Error definitions and error collector for semantic analysis.

Provides structured error reporting with source locations.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

from ..lexer.token import SourceLocation


class ErrorLevel(Enum):
    """Severity level of an error."""
    WARNING = "warning"
    ERROR = "error"


@dataclass
class SemanticError:
    """
    Represents a semantic error or warning.
    
    Includes location information and error details for helpful reporting.
    """
    level: ErrorLevel
    message: str
    location: SourceLocation
    hint: Optional[str] = None  # Suggestion for fixing the error
    
    def __str__(self) -> str:
        """Format error for display."""
        result = f"{self.level.value}: {self.location}: {self.message}"
        if self.hint:
            result += f"\n  hint: {self.hint}"
        return result
    
    def __repr__(self) -> str:
        return self.__str__()


class ErrorCollector:
    """
    Collects errors and warnings during semantic analysis.
    
    Allows multiple passes to report errors without immediately failing,
    providing comprehensive error reporting.
    """
    
    def __init__(self):
        """Initialize empty error collector."""
        self.errors: List[SemanticError] = []
        self.warnings: List[SemanticError] = []
    
    def error(self, message: str, location: SourceLocation, hint: Optional[str] = None):
        """Add an error."""
        err = SemanticError(ErrorLevel.ERROR, message, location, hint)
        self.errors.append(err)
    
    def warning(self, message: str, location: SourceLocation, hint: Optional[str] = None):
        """Add a warning."""
        warn = SemanticError(ErrorLevel.WARNING, message, location, hint)
        self.warnings.append(warn)
    
    def has_errors(self) -> bool:
        """Check if any errors were reported."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if any warnings were reported."""
        return len(self.warnings) > 0
    
    def get_all(self) -> List[SemanticError]:
        """Get all errors and warnings, sorted by location."""
        all_issues = self.errors + self.warnings
        return sorted(all_issues, key=lambda e: (e.location.line, e.location.column))
    
    def clear(self):
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()
    
    def report(self) -> str:
        """Generate formatted error report."""
        if not self.has_errors() and not self.has_warnings():
            return "No errors or warnings"
        
        lines = []
        
        if self.has_errors():
            lines.append(f"Found {len(self.errors)} error(s):")
            for err in self.errors:
                lines.append(str(err))
        
        if self.has_warnings():
            if lines:
                lines.append("")
            lines.append(f"Found {len(self.warnings)} warning(s):")
            for warn in self.warnings:
                lines.append(str(warn))
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.report()


# Common error types for convenience

class TypeErrors:
    """Factory methods for common type errors."""
    
    @staticmethod
    def type_mismatch(expected: str, actual: str, location: SourceLocation) -> SemanticError:
        """Type mismatch error."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Type mismatch: expected {expected}, got {actual}",
            location,
            f"Convert the value to {expected} or change the expected type"
        )
    
    @staticmethod
    def undefined_variable(name: str, location: SourceLocation) -> SemanticError:
        """Undefined variable error."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Undefined variable: '{name}'",
            location,
            f"Declare variable '{name}' before using it"
        )
    
    @staticmethod
    def undefined_function(name: str, location: SourceLocation) -> SemanticError:
        """Undefined function error."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Undefined function: '{name}'",
            location,
            f"Define function '{name}' before calling it"
        )
    
    @staticmethod
    def redefinition(name: str, kind: str, location: SourceLocation) -> SemanticError:
        """Redefinition error."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Redefinition of {kind} '{name}'",
            location,
            f"Choose a different name or remove one of the definitions"
        )
    
    @staticmethod
    def immutable_assignment(name: str, location: SourceLocation) -> SemanticError:
        """Assignment to immutable variable."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Cannot assign to val '{name}'",
            location,
            f"Use 'var' instead of 'val' if you need to reassign"
        )
    
    @staticmethod
    def wrong_argument_count(
        expected: int, actual: int, func_name: str, location: SourceLocation
    ) -> SemanticError:
        """Wrong number of arguments."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Function '{func_name}' expects {expected} argument(s), got {actual}",
            location,
            f"Provide exactly {expected} argument(s)"
        )
    
    @staticmethod
    def invalid_operator(op: str, type1: str, type2: Optional[str], location: SourceLocation) -> SemanticError:
        """Invalid operator for types."""
        if type2:
            msg = f"Operator '{op}' cannot be applied to types {type1} and {type2}"
        else:
            msg = f"Unary operator '{op}' cannot be applied to type {type1}"
        
        return SemanticError(
            ErrorLevel.ERROR,
            msg,
            location,
            "Check operator compatibility with operand types"
        )
    
    @staticmethod
    def return_type_mismatch(
        expected: str, actual: str, func_name: str, location: SourceLocation
    ) -> SemanticError:
        """Return type doesn't match function signature."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Function '{func_name}' returns {actual}, but signature specifies {expected}",
            location,
            f"Change return type to {actual} or convert the return value"
        )
    
    @staticmethod
    def missing_return(func_name: str, return_type: str, location: SourceLocation) -> SemanticError:
        """Missing return statement."""
        return SemanticError(
            ErrorLevel.ERROR,
            f"Function '{func_name}' must return a value of type {return_type}",
            location,
            "Add a return statement with appropriate value"
        )
    
    @staticmethod
    def unreachable_code(location: SourceLocation) -> SemanticError:
        """Unreachable code warning."""
        return SemanticError(
            ErrorLevel.WARNING,
            "Unreachable code detected",
            location,
            "Remove this code or fix the control flow"
        )
