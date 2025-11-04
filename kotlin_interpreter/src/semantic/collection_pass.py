"""
Declaration collection pass.

First pass of semantic analysis: collects all function and variable declarations
into symbol table before type checking. This allows forward references.
"""

from typing import Dict
from ..parser.ast_nodes import *
from .symbol_table import SymbolTable, Symbol, FunctionSymbol, SymbolKind
from .errors import ErrorCollector, TypeErrors
from .type_system import TypeSystem


class CollectionPass:
    """
    Collects declarations and populates symbol table.
    
    This is the first semantic analysis pass, which:
    1. Registers all functions in global scope
    2. Registers global variables
    3. Creates function parameter symbols
    4. Validates type annotations
    """
    
    def __init__(self, symbol_table: SymbolTable, error_collector: ErrorCollector):
        """Initialize collection pass."""
        self.symbols = symbol_table
        self.errors = error_collector
    
    def collect(self, program: Program):
        """Collect declarations from program."""
        for decl in program.declarations:
            self.visit_declaration(decl)
    
    def visit_declaration(self, node: Declaration):
        """Visit a declaration node."""
        if isinstance(node, FunctionDeclaration):
            self.visit_function_declaration(node)
        elif isinstance(node, VariableDeclaration):
            self.visit_variable_declaration(node)
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        """Collect function declaration."""
        # Validate return type
        return_type = node.return_type if node.return_type else "Unit"
        if not TypeSystem.is_valid_type(return_type):
            self.errors.error(
                f"Unknown type: {return_type}",
                node.location,
                "Use Int, String, Boolean, or Unit"
            )
            return_type = "Unit"  # Fallback
        
        # Collect parameter types
        param_types = []
        for param in node.parameters:
            if not TypeSystem.is_valid_type(param.type):
                self.errors.error(
                    f"Unknown type: {param.type}",
                    param.location,
                    "Use Int, String, Boolean, or Unit"
                )
                param_types.append("Any")  # Fallback
            else:
                param_types.append(param.type)
        
        # Create function symbol
        func_symbol = FunctionSymbol(
            name=node.name,
            parameter_types=param_types,
            return_type=return_type,
            location=node.location
        )
        
        # Register in symbol table
        if not self.symbols.define(func_symbol):
            # Function already defined
            existing = self.symbols.lookup_local(node.name)
            self.errors.errors.append(
                TypeErrors.redefinition(node.name, "function", node.location)
            )
    
    def visit_variable_declaration(self, node: VariableDeclaration):
        """Collect variable declaration."""
        # Validate type annotation if present
        if node.type:
            if not TypeSystem.is_valid_type(node.type):
                self.errors.error(
                    f"Unknown type: {node.type}",
                    node.location,
                    "Use Int, String, Boolean, or Unit"
                )
                var_type = "Any"  # Fallback
            else:
                var_type = node.type
        else:
            # Type will be inferred in type checking pass
            var_type = "Any"  # Temporary placeholder
        
        # Create variable symbol
        var_symbol = Symbol(
            name=node.name,
            kind=SymbolKind.VARIABLE,
            type=var_type,
            is_mutable=node.is_mutable,
            location=node.location
        )
        
        # Register in symbol table
        if not self.symbols.define(var_symbol):
            # Variable already defined in current scope
            existing = self.symbols.lookup_local(node.name)
            self.errors.errors.append(
                TypeErrors.redefinition(node.name, "variable", node.location)
            )
