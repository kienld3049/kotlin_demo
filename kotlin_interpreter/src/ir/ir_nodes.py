"""
IR (Intermediate Representation) Nodes
Platform-independent intermediate code representation
"""
from dataclasses import dataclass
from typing import Any, List


@dataclass
class IRNode:
    """Base class for all IR nodes"""
    pass


@dataclass
class IRConstant(IRNode):
    """
    Constant assignment: var_name: type = value
    Example: a: Int = 3
    """
    var_name: str
    value: Any
    type_name: str
    
    def __str__(self):
        return f"{self.var_name}: {self.type_name} = {self.value}"


@dataclass
class IRBinaryOp(IRNode):
    """
    Binary operation: result = left op right
    Example: temp0 = a + b
    """
    result: str
    left: str
    op: str
    right: str
    
    def __str__(self):
        return f"{self.result} = {self.left} {self.op} {self.right}"


@dataclass
class IRAssignment(IRNode):
    """
    Assignment: var_name = value
    Example: c = temp0
    """
    var_name: str
    value: str
    
    def __str__(self):
        return f"{self.var_name} = {self.value}"


@dataclass
class IRFunctionCall(IRNode):
    """
    Function call: call func_name(args...)
    Example: call println(c)
    """
    func_name: str
    args: List[str]
    
    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"call {self.func_name}({args_str})"
