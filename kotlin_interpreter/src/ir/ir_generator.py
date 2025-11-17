"""
IR Generator - Converts AST to Intermediate Representation
Transform AST nodes into platform-independent IR instructions
"""
from typing import List, Optional
from .ir_nodes import IRNode, IRConstant, IRBinaryOp, IRAssignment, IRFunctionCall
from ..parser.ast_nodes import *


class IRGenerator:
    """
    Generates IR instructions from AST
    Similar to Evaluator but produces instructions instead of executing
    """
    
    def __init__(self):
        self.instructions: List[IRNode] = []
        self.temp_counter = 0
    
    def new_temp(self) -> str:
        """Generate a new temporary variable name"""
        temp = f"temp{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def generate(self, program: Program) -> List[IRNode]:
        """Main entry point - generate IR from Program AST"""
        self.instructions = []
        self.temp_counter = 0
        
        # Process all declarations in the program
        for decl in program.declarations:
            self._visit_declaration(decl)
        
        return self.instructions
    
    def _visit_declaration(self, node: Declaration):
        """Visit a declaration node"""
        if isinstance(node, FunctionDeclaration):
            # For now, only process main function body
            if node.name == "main" and node.body:
                self._visit_statement(node.body)
        
        elif isinstance(node, VariableDeclaration):
            # Top-level variable declaration
            if node.initializer:
                value_name = self._visit_expression(node.initializer)
                self.instructions.append(
                    IRAssignment(node.name, value_name)
                )
    
    def _visit_statement(self, node: Statement):
        """Visit a statement node"""
        if isinstance(node, BlockStatement):
            # Process all statements in block
            for stmt in node.statements:
                self._visit_statement(stmt)
        
        elif isinstance(node, ExpressionStatement):
            # Standalone expression (like function call)
            self._visit_expression(node.expression)
        
        elif isinstance(node, DeclarationStatement):
            # Variable declaration inside function
            decl = node.declaration
            if isinstance(decl, VariableDeclaration) and decl.initializer:
                value_name = self._visit_expression(decl.initializer)
                self.instructions.append(
                    IRAssignment(decl.name, value_name)
                )
        
        elif isinstance(node, IfStatement):
            # For IR simulation, we simplify control flow
            # Just process both branches
            self._visit_statement(node.then_branch)
            if node.else_branch:
                self._visit_statement(node.else_branch)
        
        elif isinstance(node, WhileStatement):
            # Simplified: just process body
            self._visit_statement(node.body)
        
        elif isinstance(node, ReturnStatement):
            # Return statement
            if node.value:
                value_name = self._visit_expression(node.value)
                self.instructions.append(
                    IRFunctionCall("return", [value_name])
                )
    
    def _visit_expression(self, expr: Expression) -> str:
        """
        Visit expression and return the name of variable/temp holding result
        """
        if isinstance(expr, LiteralExpression):
            # Return literal value as string
            if expr.literal_type == "String":
                return f'"{expr.value}"'
            return str(expr.value)
        
        elif isinstance(expr, IdentifierExpression):
            # Return variable name
            return expr.name
        
        elif isinstance(expr, BinaryExpression):
            # Recursively get left and right operands
            left = self._visit_expression(expr.left)
            right = self._visit_expression(expr.right)
            
            # Create temporary for result
            temp = self.new_temp()
            
            # Add binary operation instruction
            self.instructions.append(
                IRBinaryOp(temp, left, expr.operator, right)
            )
            
            return temp
        
        elif isinstance(expr, UnaryExpression):
            # Handle unary operations
            operand = self._visit_expression(expr.operand)
            temp = self.new_temp()
            
            # Convert unary to binary with 0 or false
            if expr.operator == '-':
                self.instructions.append(
                    IRBinaryOp(temp, "0", "-", operand)
                )
            elif expr.operator == '!':
                self.instructions.append(
                    IRBinaryOp(temp, operand, "==", "false")
                )
            
            return temp
        
        elif isinstance(expr, CallExpression):
            # Process arguments
            arg_names = []
            for arg in expr.arguments:
                arg_name = self._visit_expression(arg)
                arg_names.append(arg_name)
            
            # Add function call instruction
            self.instructions.append(
                IRFunctionCall(expr.function_name, arg_names)
            )
            
            # Function calls return void in IR (for simplicity)
            return "void"
        
        elif isinstance(expr, AssignmentExpression):
            # Assignment expression
            value_name = self._visit_expression(expr.value)
            self.instructions.append(
                IRAssignment(expr.target, value_name)
            )
            return expr.target
        
        elif isinstance(expr, IfExpression):
            # If expression - simplified: evaluate both branches
            then_result = self._visit_expression(expr.then_branch)
            else_result = self._visit_expression(expr.else_branch)
            
            # Create temp for result
            temp = self.new_temp()
            self.instructions.append(
                IRAssignment(temp, then_result)  # Simplified
            )
            return temp
        
        elif isinstance(expr, BlockExpression):
            # Block expression - process all statements
            result = "void"
            for stmt in expr.statements:
                if isinstance(stmt, ExpressionStatement):
                    result = self._visit_expression(stmt.expression)
                else:
                    self._visit_statement(stmt)
            return result
        
        elif isinstance(expr, StringTemplateExpression):
            # String template - simplified: concatenate parts
            parts = []
            for part in expr.parts:
                parts.append(self._visit_expression(part))
            
            temp = self.new_temp()
            # Simplified: just use first part
            if parts:
                self.instructions.append(
                    IRAssignment(temp, parts[0])
                )
            return temp
        
        # Unknown expression type
        return "unknown"
    
    def get_ir_as_text(self) -> str:
        """Return IR as formatted text"""
        if not self.instructions:
            return "(no IR instructions generated)"
        
        lines = []
        for i, instr in enumerate(self.instructions, 1):
            lines.append(f"{i}. {instr}")
        return "\n".join(lines)
