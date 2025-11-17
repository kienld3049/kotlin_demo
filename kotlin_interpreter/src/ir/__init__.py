"""
IR Module - Intermediate Representation
Converts AST to platform-independent intermediate code
"""
from .ir_nodes import IRNode, IRConstant, IRBinaryOp, IRAssignment, IRFunctionCall
from .ir_generator import IRGenerator

__all__ = [
    'IRNode',
    'IRConstant', 
    'IRBinaryOp',
    'IRAssignment',
    'IRFunctionCall',
    'IRGenerator'
]
