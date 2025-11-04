"""
Type system for Kotlin interpreter.

Defines types and type compatibility rules.
"""

from typing import Optional, Set
from dataclasses import dataclass


class KotlinType:
    """Base class for Kotlin types."""
    
    def __init__(self, name: str):
        self.name = name
    
    def is_compatible_with(self, other: 'KotlinType') -> bool:
        """Check if this type is compatible with another type."""
        return self == other
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, KotlinType):
            return False
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"KotlinType({self.name})"


# Built-in types

class IntType(KotlinType):
    """Integer type."""
    def __init__(self):
        super().__init__("Int")


class StringType(KotlinType):
    """String type."""
    def __init__(self):
        super().__init__("String")


class BooleanType(KotlinType):
    """Boolean type."""
    def __init__(self):
        super().__init__("Boolean")


class UnitType(KotlinType):
    """Unit type (similar to void)."""
    def __init__(self):
        super().__init__("Unit")


class AnyType(KotlinType):
    """
    Any type - supertype of all types.
    Used for built-in functions like println that accept any argument.
    """
    def __init__(self):
        super().__init__("Any")
    
    def is_compatible_with(self, other: KotlinType) -> bool:
        """Any is compatible with any type."""
        return True


class NothingType(KotlinType):
    """
    Nothing type - subtype of all types.
    Used for expressions that never return (infinite loops, throws).
    """
    def __init__(self):
        super().__init__("Nothing")
    
    def is_compatible_with(self, other: KotlinType) -> bool:
        """Nothing is compatible with any type."""
        return True


# Type registry - singleton instances

INT = IntType()
STRING = StringType()
BOOLEAN = BooleanType()
UNIT = UnitType()
ANY = AnyType()
NOTHING = NothingType()


class TypeSystem:
    """
    Manages type checking and type inference.
    """
    
    # Map type names to type objects
    TYPES = {
        "Int": INT,
        "String": STRING,
        "Boolean": BOOLEAN,
        "Unit": UNIT,
        "Any": ANY,
        "Nothing": NOTHING,
    }
    
    @staticmethod
    def get_type(name: str) -> Optional[KotlinType]:
        """Get type object by name."""
        return TypeSystem.TYPES.get(name)
    
    @staticmethod
    def is_valid_type(name: str) -> bool:
        """Check if type name is valid."""
        return name in TypeSystem.TYPES
    
    @staticmethod
    def is_compatible(source_type: KotlinType, target_type: KotlinType) -> bool:
        """
        Check if source type can be used where target type is expected.
        
        Examples:
        - Int is compatible with Int
        - Any is compatible with String (accepts any type)
        - Nothing is compatible with Int (never returns)
        """
        if source_type == target_type:
            return True
        
        # Any accepts everything
        if target_type == ANY:
            return True
        
        # Nothing can be used anywhere
        if source_type == NOTHING:
            return True
        
        return False
    
    @staticmethod
    def get_binary_result_type(
        left_type: KotlinType,
        operator: str,
        right_type: KotlinType
    ) -> Optional[KotlinType]:
        """
        Get result type of binary operation, or None if invalid.
        """
        # Arithmetic operators: Int op Int -> Int
        if operator in ["+", "-", "*", "/", "%"]:
            if operator == "+" and (left_type == STRING or right_type == STRING):
                # String concatenation
                return STRING
            if left_type == INT and right_type == INT:
                return INT
            return None
        
        # Comparison operators: T op T -> Boolean (for comparable types)
        if operator in ["==", "!="]:
            # Any type can be compared for equality
            if TypeSystem.is_compatible(left_type, right_type) or \
               TypeSystem.is_compatible(right_type, left_type):
                return BOOLEAN
            return None
        
        if operator in ["<", "<=", ">", ">="]:
            # Only Int can be ordered
            if left_type == INT and right_type == INT:
                return BOOLEAN
            return None
        
        # Logical operators: Boolean op Boolean -> Boolean
        if operator in ["&&", "||"]:
            if left_type == BOOLEAN and right_type == BOOLEAN:
                return BOOLEAN
            return None
        
        return None
    
    @staticmethod
    def get_unary_result_type(
        operator: str,
        operand_type: KotlinType
    ) -> Optional[KotlinType]:
        """
        Get result type of unary operation, or None if invalid.
        """
        # Negation: -Int -> Int
        if operator == "-":
            if operand_type == INT:
                return INT
            return None
        
        # Logical NOT: !Boolean -> Boolean
        if operator == "!":
            if operand_type == BOOLEAN:
                return BOOLEAN
            return None
        
        return None
    
    @staticmethod
    def infer_literal_type(value) -> KotlinType:
        """Infer type from literal value."""
        if isinstance(value, int):
            return INT
        elif isinstance(value, str):
            return STRING
        elif isinstance(value, bool):
            return BOOLEAN
        elif value is None:
            return UNIT
        else:
            raise ValueError(f"Cannot infer type for value: {value}")
    
    @staticmethod
    def can_assign(target_type: KotlinType, source_type: KotlinType) -> bool:
        """
        Check if source can be assigned to target.
        
        This is similar to is_compatible but may have different rules
        for assignment vs function calls.
        """
        return TypeSystem.is_compatible(source_type, target_type)
    
    @staticmethod
    def common_supertype(type1: KotlinType, type2: KotlinType) -> KotlinType:
        """
        Find common supertype for two types.
        Used in if expressions to determine result type.
        """
        if type1 == type2:
            return type1
        
        # If either is Nothing, return the other
        if type1 == NOTHING:
            return type2
        if type2 == NOTHING:
            return type1
        
        # Otherwise, fall back to Any
        return ANY
