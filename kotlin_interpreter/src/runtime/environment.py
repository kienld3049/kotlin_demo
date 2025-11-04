"""
Runtime environment for variable storage.

Manages variable scopes during program execution.
"""

from typing import Dict, Optional
from .runtime_objects import RuntimeValue


class Environment:
    """
    Runtime environment for storing variables.
    
    Implements lexical scoping with parent pointers.
    Similar to SymbolTable but for runtime values instead of symbols.
    """
    
    def __init__(self, parent: Optional['Environment'] = None):
        """
        Initialize environment.
        
        Args:
            parent: Parent environment for nested scopes
        """
        self.parent = parent
        self.variables: Dict[str, RuntimeValue] = {}
    
    def define(self, name: str, value: RuntimeValue):
        """
        Define a new variable in this environment.
        
        Args:
            name: Variable name
            value: Runtime value to store
        """
        self.variables[name] = value
    
    def get(self, name: str) -> RuntimeValue:
        """
        Get variable value, searching parent scopes if needed.
        
        Args:
            name: Variable name
            
        Returns:
            Runtime value
            
        Raises:
            RuntimeError: If variable is not defined
        """
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise RuntimeError(f"Undefined variable: '{name}'")
    
    def set(self, name: str, value: RuntimeValue):
        """
        Set variable value, searching parent scopes if needed.
        
        Args:
            name: Variable name
            value: New runtime value
            
        Raises:
            RuntimeError: If variable is not defined
        """
        if name in self.variables:
            self.variables[name] = value
            return
        
        if self.parent:
            self.parent.set(name, value)
            return
        
        raise RuntimeError(f"Undefined variable: '{name}'")
    
    def has(self, name: str) -> bool:
        """Check if variable exists in this environment or parents."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False
    
    def has_local(self, name: str) -> bool:
        """Check if variable exists in this environment only."""
        return name in self.variables
    
    def __repr__(self) -> str:
        vars_str = ", ".join(self.variables.keys())
        parent_str = "with parent" if self.parent else "no parent"
        return f"Environment([{vars_str}], {parent_str})"
