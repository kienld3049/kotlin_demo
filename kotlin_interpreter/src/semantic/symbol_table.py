"""
Symbol table for tracking variables and functions.

Manages scopes and symbol resolution during semantic analysis.
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum

from ..lexer.token import SourceLocation


class SymbolKind(Enum):
    """Kind of symbol."""
    VARIABLE = "variable"
    FUNCTION = "function"
    PARAMETER = "parameter"


@dataclass
class Symbol:
    """
    Represents a symbol (variable, function, etc.) in the symbol table.
    """
    name: str
    kind: SymbolKind
    type: str  # Type name (Int, String, Boolean, etc.)
    is_mutable: bool  # For variables: val vs var
    location: SourceLocation  # Where it was declared
    
    def __repr__(self) -> str:
        mut = "var" if self.is_mutable else "val"
        return f"{self.kind.value} {mut} {self.name}: {self.type}"


@dataclass
class FunctionSymbol(Symbol):
    """Function symbol with parameter information."""
    parameter_types: List[str]
    return_type: str
    
    def __init__(
        self,
        name: str,
        parameter_types: List[str],
        return_type: str,
        location: SourceLocation
    ):
        super().__init__(
            name=name,
            kind=SymbolKind.FUNCTION,
            type=return_type,  # Function's type is its return type
            is_mutable=False,  # Functions aren't mutable
            location=location
        )
        self.parameter_types = parameter_types
        self.return_type = return_type
    
    def __repr__(self) -> str:
        params = ", ".join(self.parameter_types)
        return f"fun {self.name}({params}): {self.return_type}"


class Scope:
    """
    Represents a lexical scope (function body, block, etc.).
    
    Scopes are organized hierarchically with parent pointers.
    """
    
    def __init__(self, name: str, parent: Optional['Scope'] = None):
        """Initialize scope."""
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, symbol: Symbol) -> bool:
        """
        Define a symbol in this scope.
        
        Returns True if successful, False if symbol already exists.
        """
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up symbol in this scope only."""
        return self.symbols.get(name)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Look up symbol in this scope and parent scopes.
        
        Implements lexical scoping.
        """
        symbol = self.lookup_local(name)
        if symbol:
            return symbol
        
        if self.parent:
            return self.parent.lookup(name)
        
        return None
    
    def __repr__(self) -> str:
        return f"Scope({self.name}, {len(self.symbols)} symbols)"


class SymbolTable:
    """
    Manages symbol tables with hierarchical scopes.
    
    Tracks the current scope and provides methods for entering/exiting scopes.
    """
    
    def __init__(self):
        """Initialize with global scope."""
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        
        # Add built-in functions
        self._add_builtins()
    
    def _add_builtins(self):
        """Add built-in functions to global scope."""
        # println function - accepts any type, returns Unit
        println_loc = SourceLocation("<builtin>", 0, 0)
        println = FunctionSymbol(
            name="println",
            parameter_types=["Any"],  # Simplified: accepts any single argument
            return_type="Unit",
            location=println_loc
        )
        self.global_scope.define(println)
        
        # print function - similar to println but no newline
        print_loc = SourceLocation("<builtin>", 0, 0)
        print_fn = FunctionSymbol(
            name="print",
            parameter_types=["Any"],
            return_type="Unit",
            location=print_loc
        )
        self.global_scope.define(print_fn)
    
    def enter_scope(self, name: str):
        """Enter a new scope."""
        new_scope = Scope(name, parent=self.current_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """Exit current scope, return to parent."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        else:
            raise RuntimeError("Cannot exit global scope")
    
    def define(self, symbol: Symbol) -> bool:
        """
        Define symbol in current scope.
        
        Returns True if successful, False if already defined.
        """
        return self.current_scope.define(symbol)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up symbol in current scope chain."""
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up symbol in current scope only."""
        return self.current_scope.lookup_local(name)
    
    def is_global_scope(self) -> bool:
        """Check if we're in global scope."""
        return self.current_scope == self.global_scope
    
    def get_scope_chain(self) -> List[Scope]:
        """Get list of scopes from current to global."""
        chain = []
        scope = self.current_scope
        while scope:
            chain.append(scope)
            scope = scope.parent
        return chain
    
    def __repr__(self) -> str:
        chain = self.get_scope_chain()
        scope_names = " -> ".join(s.name for s in reversed(chain))
        return f"SymbolTable(current: {scope_names})"
