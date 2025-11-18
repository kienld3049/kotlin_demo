"""
State Manager for Streamlit Kotlin Interpreter GUI
Quản lý trạng thái của ứng dụng và tương tác với interpreter
"""

import streamlit as st
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.collection_pass import CollectionPass
from src.semantic.symbol_table import SymbolTable
from src.semantic.errors import ErrorCollector
from src.runtime.evaluator import Evaluator
from src.runtime.environment import Environment
from src.ir.ir_generator import IRGenerator
from src.codegen.generators import JVMBytecodeGenerator, JavaScriptGenerator, NativeCodeGenerator


@dataclass
class InterpreterState:
    """Lưu trữ trạng thái của interpreter"""
    source_code: str = ""
    tokens: List = field(default_factory=list)
    ast: Optional[Any] = None
    symbol_table: Optional[SymbolTable] = None
    ir_instructions: List = field(default_factory=list)
    jvm_code: str = ""
    js_code: str = ""
    native_code: str = ""
    output: str = ""
    errors: List[str] = field(default_factory=list)
    execution_steps: List[Dict] = field(default_factory=list)
    current_step: int = 0


class StateManager:
    """Quản lý state của Streamlit app"""
    
    @staticmethod
    def initialize():
        """Khởi tạo session state nếu chưa có"""
        if 'interpreter_state' not in st.session_state:
            # Khởi tạo với Hello World example làm default
            default_code = '''fun main() {
        println("Hello, World!")
    }'''
            st.session_state.interpreter_state = InterpreterState(
                source_code=default_code  # ← Set default code
            )
        
        if 'show_details' not in st.session_state:
            st.session_state.show_details = True
        
        if 'auto_run' not in st.session_state:
            st.session_state.auto_run = False

    
    @staticmethod
    def get_state() -> InterpreterState:
        """Lấy state hiện tại"""
        return st.session_state.interpreter_state
    
    @staticmethod
    def update_source_code(code: str):
        """Cập nhật source code"""
        st.session_state.interpreter_state.source_code = code
    
    @staticmethod
    def clear_state():
        """Xóa state và reset về ban đầu"""
        st.session_state.interpreter_state = InterpreterState()
    
    @staticmethod
    def run_interpreter(source_code: str) -> Dict[str, Any]:
        """
        Chạy interpreter với source code
        Returns dict với keys: success, tokens, ast, symbol_table, ir_instructions, jvm_code, js_code, native_code, output, errors
        """
        result = {
            'success': False,
            'tokens': [],
            'ast': None,
            'symbol_table': None,
            'ir_instructions': [],
            'jvm_code': '',
            'js_code': '',
            'native_code': '',
            'output': '',
            'errors': []
        }
        
        try:
            # Step 1: Lexical Analysis
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            result['tokens'] = tokens
            
            # Step 2: Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            result['ast'] = ast
            
            # Step 3: Semantic Analysis
            symbol_table = SymbolTable()
            error_collector = ErrorCollector()
            collection_pass = CollectionPass(symbol_table, error_collector)
            collection_pass.collect(ast)
            
            # Check for semantic errors
            if error_collector.has_errors():
                for error in error_collector.errors:
                    result['errors'].append(str(error))
            
            result['symbol_table'] = symbol_table
            
            # Step 4: IR Generation
            ir_generator = IRGenerator()
            ir_instructions = ir_generator.generate(ast)
            result['ir_instructions'] = ir_instructions
            
            # Step 5: Code Generation
            jvm_generator = JVMBytecodeGenerator(ir_instructions)
            result['jvm_code'] = jvm_generator.generate()
            
            js_generator = JavaScriptGenerator(ir_instructions)
            result['js_code'] = js_generator.generate()
            
            native_generator = NativeCodeGenerator(ir_instructions)
            result['native_code'] = native_generator.generate()
            
            # Step 6: Execution
            evaluator = Evaluator()
            
            # Capture output
            import io
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                evaluator.evaluate(ast)
            
            result['output'] = output_buffer.getvalue()
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
            result['success'] = False
        
        # Update state
        state = StateManager.get_state()
        state.source_code = source_code
        state.tokens = result['tokens']
        state.ast = result['ast']
        state.symbol_table = result['symbol_table']
        state.ir_instructions = result['ir_instructions']
        state.jvm_code = result['jvm_code']
        state.js_code = result['js_code']
        state.native_code = result['native_code']
        state.output = result['output']
        state.errors = result['errors']
        
        return result
    
    @staticmethod
    def get_example_programs() -> Dict[str, str]:
        """Trả về danh sách các chương trình mẫu"""
        return {
            # === Basic Examples ===
            "Hello World": '''fun main() {
    println("Hello, World!")
}''',
            "Variables": '''fun main() {
    val x = 10
    var y = 20
    y = y + x
    println("x = " + x)
    println("y = " + y)
}''',
            "Functions": '''fun add(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val result = add(5, 3)
    println("5 + 3 = " + result)
}''',
            "If Expression": '''fun main() {
    val x = 10
    val result = if (x > 5) {
        "x is greater than 5"
    } else {
        "x is less than or equal to 5"
    }
    println(result)
}''',
            "While Loop": '''fun main() {
    var count = 0
    while (count < 5) {
        println("Count: " + count)
        count = count + 1
    }
}''',
            
            # === Gemini Test Cases ===
            "Test 1: Sanity Check": '''fun main() {
    val a = 10
    var b = 20
    b = a + b
    println("a = " + a)
    println("b = " + b)
}''',
            "Test 2: Scope & Shadowing": '''fun main() {
    var i = 1
    val x = 100
    
    println("Start loop, global x = " + x)

    while (i <= 3) {
        val y = i * 10
        var x = 5
        
        println("Loop " + i + ": y = " + y + ", inner x = " + x)
        
        x = x + y
        println("Loop " + i + ": new inner x = " + x)
        
        i = i + 1
    }
    
    println("End loop, global x = " + x)
}''',
            "Test 3: Factorial (Recursion)": '''fun factorial(n: Int): Int {
    if (n <= 1) {
        return 1
    }
    
    val result = n * factorial(n - 1)
    
    return result
}

fun main() {
    println("--- Function Test ---")
    val fact5 = factorial(5)
    println("Factorial of 5 is " + fact5)
}''',
            "Test 4a: Undefined Variable": '''fun main() {
    println(bi_chua_khai_bao)
}''',
            "Test 4b: Invalid Operands": '''fun main() {
    val x = 10 - "hello"
    println(x)
}''',
            "Test 4c: Division by Zero": '''fun main() {
    val y = 100 / 0
    println(y)
}'''
        }
