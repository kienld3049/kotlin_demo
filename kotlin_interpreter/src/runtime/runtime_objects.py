"""
Runtime value objects for Kotlin interpreter.

Represents values at runtime with type information.
"""

from typing import Any, List, Optional, Callable
from dataclasses import dataclass


@dataclass
class RuntimeValue:
    """
    Base class for runtime values.
    
    All values in the interpreter are wrapped in RuntimeValue objects
    that track their type and provide a consistent interface.
    """
    value: Any
    type_name: str
    
    def __str__(self) -> str:
        """String representation for display."""
        if self.type_name == "Unit":
            return "kotlin.Unit"
        elif self.type_name == "String":
            return self.value
        elif self.type_name == "Boolean":
            return "true" if self.value else "false"
        else:
            return str(self.value)
    
    def __repr__(self) -> str:
        return f"RuntimeValue({self.value!r}, {self.type_name})"
    
    def is_truthy(self) -> bool:
        """
        Determine truthiness of value.
        Used for conditions in if/while statements.
        """
        if self.type_name == "Boolean":
            return self.value
        # In our simple interpreter, only Boolean can be used in conditions
        raise RuntimeError(f"Type {self.type_name} cannot be used as condition")


@dataclass
class IntValue(RuntimeValue):
    """Integer runtime value."""
    def __init__(self, value: int):
        super().__init__(value, "Int")


@dataclass
class StringValue(RuntimeValue):
    """String runtime value."""
    def __init__(self, value: str):
        super().__init__(value, "String")


@dataclass
class BooleanValue(RuntimeValue):
    """Boolean runtime value."""
    def __init__(self, value: bool):
        super().__init__(value, "Boolean")


@dataclass
class UnitValue(RuntimeValue):
    """Unit runtime value (void/null)."""
    def __init__(self):
        super().__init__(None, "Unit")


@dataclass
class FunctionValue(RuntimeValue):
    """
    Function runtime value.
    
    Stores function definition for later execution.
    """
    parameters: List[str]  # Parameter names
    body: Any  # AST node for function body (BlockStatement)
    closure_env: Any  # Environment where function was defined (for closures)
    
    def __init__(self, parameters: List[str], body: Any, closure_env: Any):
        super().__init__(None, "Function")
        self.parameters = parameters
        self.body = body
        self.closure_env = closure_env
    
    def __str__(self) -> str:
        param_list = ", ".join(self.parameters)
        return f"<function({param_list})>"


@dataclass
class BuiltinFunctionValue(RuntimeValue):
    """
    Built-in function runtime value.
    
    Wraps native Python functions as Kotlin functions.
    """
    func: Callable
    name: str
    
    def __init__(self, name: str, func: Callable):
        super().__init__(None, "Function")
        self.name = name
        self.func = func
    
    def call(self, args: List[RuntimeValue]) -> RuntimeValue:
        """Call the built-in function."""
        return self.func(args)
    
    def __str__(self) -> str:
        return f"<builtin {self.name}>"


# Helper functions for creating runtime values

def make_int(value: int) -> IntValue:
    """Create integer runtime value."""
    return IntValue(value)


def make_string(value: str) -> StringValue:
    """Create string runtime value."""
    return StringValue(value)


def make_boolean(value: bool) -> BooleanValue:
    """Create boolean runtime value."""
    return BooleanValue(value)


def make_unit() -> UnitValue:
    """Create unit runtime value."""
    return UnitValue()


def make_function(parameters: List[str], body: Any, closure_env: Any) -> FunctionValue:
    """Create function runtime value."""
    return FunctionValue(parameters, body, closure_env)


def make_builtin(name: str, func: Callable) -> BuiltinFunctionValue:
    """Create built-in function runtime value."""
    return BuiltinFunctionValue(name, func)


# Type checking helpers

def is_int(value: RuntimeValue) -> bool:
    """Check if value is integer."""
    return value.type_name == "Int"


def is_string(value: RuntimeValue) -> bool:
    """Check if value is string."""
    return value.type_name == "String"


def is_boolean(value: RuntimeValue) -> bool:
    """Check if value is boolean."""
    return value.type_name == "Boolean"


def is_unit(value: RuntimeValue) -> bool:
    """Check if value is unit."""
    return value.type_name == "Unit"


def is_function(value: RuntimeValue) -> bool:
    """Check if value is function."""
    return value.type_name == "Function"
