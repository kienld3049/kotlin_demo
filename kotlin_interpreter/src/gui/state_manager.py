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


@dataclass
class InterpreterState:
    """Lưu trữ trạng thái của interpreter"""
    source_code: str = ""
    tokens: List = field(default_factory=list)
    ast: Optional[Any] = None
    symbol_table: Optional[SymbolTable] = None
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
            st.session_state.interpreter_state = InterpreterState()
        
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
        Returns dict với keys: success, tokens, ast, symbol_table, output, errors
        """
        result = {
            'success': False,
            'tokens': [],
            'ast': None,
            'symbol_table': None,
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
            
            # Step 4: Execution
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
        state.output = result['output']
        state.errors = result['errors']
        
        return result
    
    @staticmethod
    def get_example_programs() -> Dict[str, str]:
        """Trả về danh sách các chương trình mẫu"""
        return {
            "Hello World": '''fun main() {
    println("Hello, World!")
}''',
            "Variables": '''fun main() {
    val x = 10
    var y = 20
    y = y + x
    println("x = $x")
    println("y = $y")
}''',
            "Functions": '''fun add(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val result = add(5, 3)
    println("5 + 3 = $result")
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
            "When Expression": '''fun main() {
    val x = 2
    val result = when (x) {
        1 -> "One"
        2 -> "Two"
        3 -> "Three"
        else -> "Other"
    }
    println("x is $result")
}''',
            "For Loop": '''fun main() {
    for (i in 1..5) {
        println("Iteration $i")
    }
}''',
            "While Loop": '''fun main() {
    var count = 0
    while (count < 5) {
        println("Count: $count")
        count = count + 1
    }
}''',
            "Lists": '''fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    println("First: ${numbers[0]}")
    println("Size: ${numbers.size}")
}''',
            "Null Safety": '''fun main() {
    val name: String? = "Kotlin"
    val length = name?.length ?: 0
    println("Length: $length")
}''',
            "Classes": '''class Person(val name: String, var age: Int) {
    fun greet() {
        println("Hello, I'm $name and I'm $age years old")
    }
}

fun main() {
    val person = Person("Alice", 25)
    person.greet()
}'''
        }
