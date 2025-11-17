"""
Code Generators - Convert IR to target platform code
Simulates code generation for JVM, JavaScript, and Native platforms
"""
from typing import List
from ..ir.ir_nodes import IRNode, IRConstant, IRBinaryOp, IRAssignment, IRFunctionCall


class CodeGenerator:
    """Base class for code generators"""
    
    def __init__(self, instructions: List[IRNode]):
        self.instructions = instructions
    
    def generate(self) -> str:
        """Generate code - override in subclass"""
        raise NotImplementedError


class JVMBytecodeGenerator(CodeGenerator):
    """
    Generates JVM Bytecode (simplified simulation)
    Real JVM bytecode is much more complex - this is educational
    """
    
    def generate(self) -> str:
        lines = [
            ";; JVM Bytecode (Simplified Simulation)",
            ";; This is educational code showing JVM-like instructions",
            "",
            ".class public Main",
            ".super java/lang/Object",
            "",
            ".method public static main([Ljava/lang/String;)V",
            "  .limit stack 10",
            "  .limit locals 10",
            ""
        ]
        
        # Map variable names to local indices
        var_map = {}
        next_index = 1
        
        for instr in self.instructions:
            if isinstance(instr, IRAssignment):
                # Handle assignment: x = value
                value = instr.value
                
                if value.isdigit():
                    # Push constant value
                    val_int = int(value)
                    if val_int <= 5:
                        lines.append(f"  iconst_{val_int}  ; push constant {val_int}")
                    else:
                        lines.append(f"  bipush {val_int}  ; push constant {val_int}")
                elif value.startswith('"'):
                    # String literal
                    lines.append(f"  ldc {value}  ; load string constant")
                else:
                    # Load from another variable
                    src_idx = var_map.get(value, 0)
                    lines.append(f"  iload {src_idx}  ; load {value}")
                
                # Store to destination variable
                if instr.var_name not in var_map:
                    var_map[instr.var_name] = next_index
                    next_index += 1
                
                dest_idx = var_map[instr.var_name]
                lines.append(f"  istore {dest_idx}  ; store to {instr.var_name}")
                lines.append("")
            
            elif isinstance(instr, IRBinaryOp):
                # Binary operation: result = left op right
                lines.append(f"  ; Compute: {instr.result} = {instr.left} {instr.op} {instr.right}")
                
                # Load left operand
                if instr.left.isdigit():
                    val = int(instr.left)
                    if val <= 5:
                        lines.append(f"  iconst_{val}")
                    else:
                        lines.append(f"  bipush {val}")
                else:
                    left_idx = var_map.get(instr.left, 0)
                    lines.append(f"  iload {left_idx}  ; load {instr.left}")
                
                # Load right operand
                if instr.right.isdigit():
                    val = int(instr.right)
                    if val <= 5:
                        lines.append(f"  iconst_{val}")
                    else:
                        lines.append(f"  bipush {val}")
                else:
                    right_idx = var_map.get(instr.right, 0)
                    lines.append(f"  iload {right_idx}  ; load {instr.right}")
                
                # Perform operation
                op_map = {
                    '+': 'iadd',
                    '-': 'isub',
                    '*': 'imul',
                    '/': 'idiv',
                    '%': 'irem'
                }
                op_code = op_map.get(instr.op, 'nop')
                lines.append(f"  {op_code}  ; perform {instr.op}")
                
                # Store result
                var_map[instr.result] = next_index
                lines.append(f"  istore {next_index}  ; store to {instr.result}")
                next_index += 1
                lines.append("")
            
            elif isinstance(instr, IRFunctionCall):
                # Function call
                if instr.func_name == 'println':
                    lines.append("  ; Call println")
                    lines.append("  getstatic java/lang/System/out Ljava/io/PrintStream;")
                    
                    # Load argument
                    if instr.args:
                        arg = instr.args[0]
                        if arg.isdigit():
                            val = int(arg)
                            if val <= 5:
                                lines.append(f"  iconst_{val}")
                            else:
                                lines.append(f"  bipush {val}")
                        elif arg.startswith('"'):
                            lines.append(f"  ldc {arg}")
                        else:
                            arg_idx = var_map.get(arg, 0)
                            lines.append(f"  iload {arg_idx}  ; load {arg}")
                    
                    lines.append("  invokevirtual java/io/PrintStream/println(I)V")
                    lines.append("")
                else:
                    # Generic function call
                    lines.append(f"  ; Call {instr.func_name}")
                    lines.append(f"  invokestatic Main/{instr.func_name}")
                    lines.append("")
        
        lines.append("  return")
        lines.append(".end method")
        
        return "\n".join(lines)


class JavaScriptGenerator(CodeGenerator):
    """Generates JavaScript code from IR"""
    
    def generate(self) -> str:
        lines = [
            "// JavaScript (Generated from IR)",
            "// This code can run in browser or Node.js",
            ""
        ]
        
        for instr in self.instructions:
            if isinstance(instr, IRAssignment):
                # Variable assignment
                lines.append(f"let {instr.var_name} = {instr.value};")
            
            elif isinstance(instr, IRBinaryOp):
                # Binary operation
                lines.append(f"let {instr.result} = {instr.left} {instr.op} {instr.right};")
            
            elif isinstance(instr, IRFunctionCall):
                # Function call
                if instr.func_name == 'println':
                    arg = instr.args[0] if instr.args else ""
                    lines.append(f"console.log({arg});")
                elif instr.func_name == 'print':
                    arg = instr.args[0] if instr.args else ""
                    lines.append(f"process.stdout.write(String({arg}));")
                else:
                    args_str = ", ".join(instr.args)
                    lines.append(f"{instr.func_name}({args_str});")
        
        return "\n".join(lines)


class NativeCodeGenerator(CodeGenerator):
    """Generates Native Assembly code (pseudo/educational)"""
    
    def generate(self) -> str:
        lines = [
            "; Native Assembly (Pseudo Code)",
            "; Educational simulation of x86-64 assembly",
            "",
            "section .data",
            ""
        ]
        
        # Declare variables in data section
        declared_vars = set()
        for instr in self.instructions:
            if isinstance(instr, IRAssignment):
                if instr.var_name not in declared_vars:
                    lines.append(f"  {instr.var_name}: dq 0  ; 64-bit integer")
                    declared_vars.add(instr.var_name)
            elif isinstance(instr, IRBinaryOp):
                if instr.result not in declared_vars:
                    lines.append(f"  {instr.result}: dq 0  ; temporary")
                    declared_vars.add(instr.result)
        
        lines.append("")
        lines.append("section .text")
        lines.append("global main")
        lines.append("")
        lines.append("main:")
        
        # Generate instructions
        for instr in self.instructions:
            if isinstance(instr, IRAssignment):
                lines.append(f"  ; Assign {instr.var_name} = {instr.value}")
                if instr.value.isdigit():
                    lines.append(f"  mov rax, {instr.value}")
                else:
                    lines.append(f"  mov rax, [{instr.value}]")
                lines.append(f"  mov [{instr.var_name}], rax")
                lines.append("")
            
            elif isinstance(instr, IRBinaryOp):
                lines.append(f"  ; Compute: {instr.result} = {instr.left} {instr.op} {instr.right}")
                
                # Load left operand into rax
                if instr.left.isdigit():
                    lines.append(f"  mov rax, {instr.left}")
                else:
                    lines.append(f"  mov rax, [{instr.left}]")
                
                # Perform operation with right operand
                op_map = {
                    '+': 'add',
                    '-': 'sub',
                    '*': 'imul',
                    '/': 'idiv',
                    '%': 'idiv'  # Remainder in rdx after idiv
                }
                op_code = op_map.get(instr.op, 'nop')
                
                if instr.right.isdigit():
                    if op_code == 'imul':
                        lines.append(f"  imul rax, {instr.right}")
                    else:
                        lines.append(f"  {op_code} rax, {instr.right}")
                else:
                    if op_code == 'imul':
                        lines.append(f"  imul rax, [{instr.right}]")
                    else:
                        lines.append(f"  {op_code} rax, [{instr.right}]")
                
                # Store result
                lines.append(f"  mov [{instr.result}], rax")
                lines.append("")
            
            elif isinstance(instr, IRFunctionCall):
                lines.append(f"  ; Call {instr.func_name}")
                
                if instr.func_name == 'println':
                    # Simplified: call printf
                    if instr.args:
                        arg = instr.args[0]
                        if arg.isdigit():
                            lines.append(f"  mov rdi, {arg}")
                        else:
                            lines.append(f"  mov rdi, [{arg}]")
                    lines.append("  call printf  ; simplified println")
                else:
                    # Generic function call
                    for i, arg in enumerate(instr.args):
                        reg = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9'][i] if i < 6 else 'rax'
                        if arg.isdigit():
                            lines.append(f"  mov {reg}, {arg}")
                        else:
                            lines.append(f"  mov {reg}, [{arg}]")
                    lines.append(f"  call {instr.func_name}")
                
                lines.append("")
        
        lines.append("  ; Exit program")
        lines.append("  mov rax, 60  ; sys_exit")
        lines.append("  xor rdi, rdi  ; exit code 0")
        lines.append("  syscall")
        
        return "\n".join(lines)
