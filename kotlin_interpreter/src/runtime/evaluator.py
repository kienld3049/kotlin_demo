"""
Evaluator - executes Kotlin AST.

Visitor pattern implementation for interpreting Kotlin programs.
"""

from typing import List, Optional
from ..parser.ast_nodes import *
from .runtime_objects import *
from .environment import Environment


class ReturnException(Exception):
    """Exception used to implement return statements."""
    def __init__(self, value: RuntimeValue):
        self.value = value
        super().__init__()


class Evaluator:
    """
    Tree-walking interpreter for Kotlin.
    
    Evaluates AST nodes and produces runtime values.
    Uses visitor pattern to traverse the AST.
    """
    
    def __init__(self):
        """Initialize evaluator with global environment."""
        self.global_env = Environment()
        self.current_env = self.global_env
        
        # Add built-in functions
        self._add_builtins()
    
    def _add_builtins(self):
        """Add built-in functions to global environment."""
        # println function
        def builtin_println(args: List[RuntimeValue]) -> RuntimeValue:
            if len(args) > 0:
                print(str(args[0]))
            else:
                print()
            return make_unit()
        
        self.global_env.define("println", make_builtin("println", builtin_println))
        
        # print function (no newline)
        def builtin_print(args: List[RuntimeValue]) -> RuntimeValue:
            if len(args) > 0:
                print(str(args[0]), end='')
            return make_unit()
        
        self.global_env.define("print", make_builtin("print", builtin_print))
    
    # Main entry point
    
    def evaluate(self, program: Program) -> RuntimeValue:
        """
        Evaluate entire program.
        
        Returns result of last expression or Unit.
        """
        result = make_unit()
        
        # First pass: collect all function declarations
        for decl in program.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.eval_function_declaration(decl)
        
        # Second pass: evaluate everything (including main execution)
        for decl in program.declarations:
            if isinstance(decl, VariableDeclaration):
                result = self.eval_variable_declaration(decl)
        
        # Try to call main function if it exists
        if self.global_env.has("main"):
            main_func = self.global_env.get("main")
            if isinstance(main_func, FunctionValue):
                result = self.call_function(main_func, [])
        
        return result
    
    # Declaration evaluation
    
    def eval_function_declaration(self, node: FunctionDeclaration) -> RuntimeValue:
        """Evaluate function declaration."""
        param_names = [param.name for param in node.parameters]
        func_value = make_function(param_names, node.body, self.current_env)
        self.current_env.define(node.name, func_value)
        return make_unit()
    
    def eval_variable_declaration(self, node: VariableDeclaration) -> RuntimeValue:
        """Evaluate variable declaration."""
        # Evaluate initializer if present
        if node.initializer:
            value = self.eval_expression(node.initializer)
        else:
            # Uninitialized variables default to Unit (simplified)
            value = make_unit()
        
        self.current_env.define(node.name, value)
        return make_unit()
    
    # Statement evaluation
    
    def eval_statement(self, node: Statement) -> RuntimeValue:
        """Evaluate a statement."""
        if isinstance(node, BlockStatement):
            return self.eval_block_statement(node)
        elif isinstance(node, ExpressionStatement):
            return self.eval_expression_statement(node)
        elif isinstance(node, IfStatement):
            return self.eval_if_statement(node)
        elif isinstance(node, WhileStatement):
            return self.eval_while_statement(node)
        elif isinstance(node, ReturnStatement):
            return self.eval_return_statement(node)
        elif isinstance(node, DeclarationStatement):
            return self.eval_declaration_statement(node)
        else:
            raise RuntimeError(f"Unknown statement type: {type(node)}")
    
    def eval_block_statement(self, node: BlockStatement) -> RuntimeValue:
        """Evaluate block statement with new scope."""
        # Create new environment for block scope
        block_env = Environment(parent=self.current_env)
        previous_env = self.current_env
        self.current_env = block_env
        
        try:
            result = make_unit()
            for stmt in node.statements:
                result = self.eval_statement(stmt)
            return result
        finally:
            # Restore previous environment
            self.current_env = previous_env
    
    def eval_expression_statement(self, node: ExpressionStatement) -> RuntimeValue:
        """Evaluate expression statement."""
        return self.eval_expression(node.expression)
    
    def eval_if_statement(self, node: IfStatement) -> RuntimeValue:
        """Evaluate if statement."""
        condition = self.eval_expression(node.condition)
        
        if condition.is_truthy():
            return self.eval_statement(node.then_branch)
        elif node.else_branch:
            return self.eval_statement(node.else_branch)
        else:
            return make_unit()
    
    def eval_while_statement(self, node: WhileStatement) -> RuntimeValue:
        """Evaluate while statement."""
        result = make_unit()
        
        while True:
            condition = self.eval_expression(node.condition)
            if not condition.is_truthy():
                break
            result = self.eval_statement(node.body)
        
        return result
    
    def eval_return_statement(self, node: ReturnStatement) -> RuntimeValue:
        """Evaluate return statement."""
        if node.value:
            value = self.eval_expression(node.value)
        else:
            value = make_unit()
        
        # Use exception to unwind stack
        raise ReturnException(value)
    
    def eval_declaration_statement(self, node: DeclarationStatement) -> RuntimeValue:
        """Evaluate declaration statement (variable declaration in function body)."""
        if isinstance(node.declaration, VariableDeclaration):
            return self.eval_variable_declaration(node.declaration)
        else:
            raise RuntimeError(f"Unknown declaration type in statement: {type(node.declaration)}")
    
    # Expression evaluation
    
    def eval_expression(self, node: Expression) -> RuntimeValue:
        """Evaluate an expression."""
        if isinstance(node, LiteralExpression):
            return self.eval_literal(node)
        elif isinstance(node, IdentifierExpression):
            return self.eval_identifier(node)
        elif isinstance(node, BinaryExpression):
            return self.eval_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self.eval_unary_expression(node)
        elif isinstance(node, CallExpression):
            return self.eval_call_expression(node)
        elif isinstance(node, AssignmentExpression):
            return self.eval_assignment_expression(node)
        elif isinstance(node, IfExpression):
            return self.eval_if_expression(node)
        else:
            raise RuntimeError(f"Unknown expression type: {type(node)}")
    
    def eval_literal(self, node: LiteralExpression) -> RuntimeValue:
        """Evaluate literal expression."""
        if node.literal_type == "Int":
            return make_int(node.value)
        elif node.literal_type == "String":
            return make_string(node.value)
        elif node.literal_type == "Boolean":
            return make_boolean(node.value)
        elif node.literal_type == "Unit":
            return make_unit()
        else:
            raise RuntimeError(f"Unknown literal type: {node.literal_type}")
    
    def eval_identifier(self, node: IdentifierExpression) -> RuntimeValue:
        """Evaluate identifier expression."""
        return self.current_env.get(node.name)
    
    def eval_binary_expression(self, node: BinaryExpression) -> RuntimeValue:
        """Evaluate binary expression."""
        left = self.eval_expression(node.left)
        right = self.eval_expression(node.right)
        op = node.operator
        
        # Arithmetic operators
        if op == "+":
            if is_int(left) and is_int(right):
                return make_int(left.value + right.value)
            # String concatenation
            elif is_string(left) or is_string(right):
                return make_string(str(left) + str(right))
            else:
                raise RuntimeError(f"Invalid operands for +: {left.type_name}, {right.type_name}")
        
        elif op == "-":
            if is_int(left) and is_int(right):
                return make_int(left.value - right.value)
            else:
                raise RuntimeError(f"Invalid operands for -: {left.type_name}, {right.type_name}")
        
        elif op == "*":
            if is_int(left) and is_int(right):
                return make_int(left.value * right.value)
            else:
                raise RuntimeError(f"Invalid operands for *: {left.type_name}, {right.type_name}")
        
        elif op == "/":
            if is_int(left) and is_int(right):
                if right.value == 0:
                    raise RuntimeError("Division by zero")
                return make_int(left.value // right.value)  # Integer division
            else:
                raise RuntimeError(f"Invalid operands for /: {left.type_name}, {right.type_name}")
        
        elif op == "%":
            if is_int(left) and is_int(right):
                if right.value == 0:
                    raise RuntimeError("Modulo by zero")
                return make_int(left.value % right.value)
            else:
                raise RuntimeError(f"Invalid operands for %: {left.type_name}, {right.type_name}")
        
        # Comparison operators
        elif op == "==":
            return make_boolean(self.values_equal(left, right))
        
        elif op == "!=":
            return make_boolean(not self.values_equal(left, right))
        
        elif op == "<":
            if is_int(left) and is_int(right):
                return make_boolean(left.value < right.value)
            else:
                raise RuntimeError(f"Invalid operands for <: {left.type_name}, {right.type_name}")
        
        elif op == "<=":
            if is_int(left) and is_int(right):
                return make_boolean(left.value <= right.value)
            else:
                raise RuntimeError(f"Invalid operands for <=: {left.type_name}, {right.type_name}")
        
        elif op == ">":
            if is_int(left) and is_int(right):
                return make_boolean(left.value > right.value)
            else:
                raise RuntimeError(f"Invalid operands for >: {left.type_name}, {right.type_name}")
        
        elif op == ">=":
            if is_int(left) and is_int(right):
                return make_boolean(left.value >= right.value)
            else:
                raise RuntimeError(f"Invalid operands for >=: {left.type_name}, {right.type_name}")
        
        # Logical operators
        elif op == "&&":
            if is_boolean(left) and is_boolean(right):
                return make_boolean(left.value and right.value)
            else:
                raise RuntimeError(f"Invalid operands for &&: {left.type_name}, {right.type_name}")
        
        elif op == "||":
            if is_boolean(left) and is_boolean(right):
                return make_boolean(left.value or right.value)
            else:
                raise RuntimeError(f"Invalid operands for ||: {left.type_name}, {right.type_name}")
        
        else:
            raise RuntimeError(f"Unknown binary operator: {op}")
    
    def eval_unary_expression(self, node: UnaryExpression) -> RuntimeValue:
        """Evaluate unary expression."""
        operand = self.eval_expression(node.operand)
        op = node.operator
        
        if op == "-":
            if is_int(operand):
                return make_int(-operand.value)
            else:
                raise RuntimeError(f"Invalid operand for -: {operand.type_name}")
        
        elif op == "!":
            if is_boolean(operand):
                return make_boolean(not operand.value)
            else:
                raise RuntimeError(f"Invalid operand for !: {operand.type_name}")
        
        else:
            raise RuntimeError(f"Unknown unary operator: {op}")
    
    def eval_call_expression(self, node: CallExpression) -> RuntimeValue:
        """Evaluate function call."""
        # Get function value
        func = self.current_env.get(node.function_name)
        
        # Evaluate arguments
        args = [self.eval_expression(arg) for arg in node.arguments]
        
        # Call function
        if isinstance(func, BuiltinFunctionValue):
            return func.call(args)
        elif isinstance(func, FunctionValue):
            return self.call_function(func, args)
        else:
            raise RuntimeError(f"'{node.function_name}' is not a function")
    
    def eval_assignment_expression(self, node: AssignmentExpression) -> RuntimeValue:
        """Evaluate assignment expression."""
        value = self.eval_expression(node.value)
        self.current_env.set(node.name, value)
        return value
    
    def eval_if_expression(self, node: IfExpression) -> RuntimeValue:
        """Evaluate if expression."""
        condition = self.eval_expression(node.condition)
        
        if condition.is_truthy():
            return self.eval_expression(node.then_branch)
        else:
            return self.eval_expression(node.else_branch)
    
    # Helper methods
    
    def call_function(self, func: FunctionValue, args: List[RuntimeValue]) -> RuntimeValue:
        """Call a user-defined function."""
        # Check argument count
        if len(args) != len(func.parameters):
            raise RuntimeError(
                f"Function expects {len(func.parameters)} arguments, got {len(args)}"
            )
        
        # Create new environment for function execution
        func_env = Environment(parent=func.closure_env)
        
        # Bind parameters
        for param_name, arg_value in zip(func.parameters, args):
            func_env.define(param_name, arg_value)
        
        # Save and switch environment
        previous_env = self.current_env
        self.current_env = func_env
        
        try:
            # Execute function body
            result = self.eval_statement(func.body)
            return result
        except ReturnException as ret:
            # Return statement was executed
            return ret.value
        finally:
            # Restore environment
            self.current_env = previous_env
    
    def values_equal(self, left: RuntimeValue, right: RuntimeValue) -> bool:
        """Check if two runtime values are equal."""
        if left.type_name != right.type_name:
            return False
        return left.value == right.value
