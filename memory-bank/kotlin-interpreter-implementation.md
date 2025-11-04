# Kotlin Interpreter - Implementation Guide

## 🛠️ Implementation Details

### Key Technical Decisions (Based on Gemini 2.5 Feedback)

#### 1. Stack-based Symbol Table Management
**Challenge**: Quản lý nested scopes (functions, blocks, if/while)

**Solution**: 
- Sử dụng Stack of Symbol Tables
- Mỗi scope có parent pointer
- Name resolution từ current scope lên parent scopes

**Benefits**:
- ✅ Correct handling của nested scopes
- ✅ Support for shadowing variables
- ✅ Clean scope entry/exit logic

#### 2. Multi-Pass Semantic Analysis
**Challenge**: Type inference với forward references (e.g., `val x = add(5, 3)`)

**Solution**:
- **Pass 1**: Collection - Thu thập function signatures
- **Pass 2**: Type Checking - Kiểm tra types với full context

**Benefits**:
- ✅ Forward references work
- ✅ Better error messages
- ✅ Proper type inference

#### 3. Hybrid Runtime Object Model
**Challenge**: Dùng Python types hay custom objects?

**Solution**: Hybrid approach
- Wrap Python types trong KotlinObject classes
- Retain Python performance
- Add Kotlin semantics layer

**Benefits**:
- ✅ Type safety enforcement
- ✅ Extensible for future features
- ✅ Clean abstraction

#### 4. Error Collection System
**Challenge**: Compiler không được crash

**Solution**: ErrorCollector pattern
- Collect all errors instead of throwing
- Report all errors at once
- User-friendly error messages với location info

**Benefits**:
- ✅ Better developer experience
- ✅ See all errors at once
- ✅ Professional compiler behavior

## 📋 Implementation Roadmap

### Phase 1: Lexer (1-2 days)

**Files to create**:
- `src/lexer/token.py`
- `src/lexer/lexer.py`
- `tests/test_lexer.py`

**Implementation steps**:
1. Define TokenType enum với tất cả tokens
2. Implement Token và SourceLocation dataclasses
3. Create Lexer class:
   - `__init__(source_code: str)`
   - `tokenize() -> List[Token]`
   - Private methods: `_read_char()`, `_peek_char()`, `_skip_whitespace()`
4. Handle keywords vs identifiers
5. Handle string literals với escape sequences
6. Track line/column accurately
7. Write comprehensive tests

**Test cases**:
```python
def test_simple_tokens():
    lexer = Lexer("fun main() { }")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.FUN
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "main"
    
def test_string_literal():
    lexer = Lexer('"Hello World"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING_LITERAL
    assert tokens[0].value == "Hello World"
    
def test_location_tracking():
    lexer = Lexer("val x = 5")
    tokens = lexer.tokenize()
    assert tokens[0].location.line == 1
    assert tokens[0].location.column == 1
```

### Phase 2: Parser (2-3 days)

**Files to create**:
- `src/parser/ast_nodes.py`
- `src/parser/parser.py`
- `tests/test_parser.py`

**Implementation steps**:
1. Define all AST node classes với dataclasses
2. Implement Parser với recursive descent
3. Methods cho mỗi grammar rule:
   - `parse_program()`
   - `parse_function_decl()`
   - `parse_statement()`
   - `parse_expression()`
   - etc.
4. Error recovery mechanisms
5. Build complete AST
6. Write tests for each grammar rule

**Example parser method**:
```python
def parse_val_decl(self) -> ValDecl:
    """val IDENTIFIER (: type)? = expression"""
    location = self.current_token.location
    self.consume(TokenType.VAL)
    
    name = self.consume(TokenType.IDENTIFIER).value
    
    declared_type = None
    if self.match(TokenType.COLON):
        declared_type = self.parse_type()
    
    self.consume(TokenType.ASSIGN)
    initializer = self.parse_expression()
    
    return ValDecl(name, declared_type, initializer, location)
```

### Phase 3a: Symbol Tables (2 days)

**Files to create**:
- `src/semantic/symbol_table.py`
- `src/semantic/scope_manager.py`
- `tests/test_scope_management.py`

**Implementation steps**:
1. Define Symbol class
2. Implement SymbolTable với parent pointer
3. Create ScopeManager class
4. Test scope push/pop
5. Test name resolution across scopes
6. Test shadowing behavior

**Test cases**:
```python
def test_nested_scopes():
    manager = ScopeManager()
    manager.define(Symbol("x", "Int", False))
    
    manager.push_scope("inner")
    manager.define(Symbol("y", "String", False))
    
    # Can resolve both x and y from inner scope
    assert manager.resolve("x").type == "Int"
    assert manager.resolve("y").type == "String"
    
    manager.pop_scope()
    
    # Can only resolve x from outer scope
    assert manager.resolve("x").type == "Int"
    assert manager.resolve("y") is None
```

### Phase 3b: Type System (3 days)

**Files to create**:
- `src/semantic/type_system.py`
- `src/semantic/collection_pass.py`
- `src/semantic/type_checker_pass.py`
- `src/utils/errors.py`
- `src/utils/error_collector.py`
- `tests/test_type_inference.py`

**Implementation steps**:
1. Define all error classes
2. Implement ErrorCollector
3. Create CollectionPhase visitor
4. Create TypeCheckingPhase visitor
5. Implement type inference logic
6. Handle binary operators type checking
7. Test comprehensive type scenarios

**Example type inference**:
```python
def test_type_inference():
    code = """
    val x = 5
    val y = x + 10
    """
    # Should infer x: Int and y: Int
    
def test_type_mismatch():
    code = """
    val x: Int = "hello"
    """
    # Should collect TypeMismatchError
```

### Phase 4a: Runtime Model (2 days)

**Files to create**:
- `src/interpreter/runtime_objects.py`
- `src/interpreter/environment.py`
- `tests/test_runtime_objects.py`

**Implementation steps**:
1. Define KotlinObject base class
2. Implement KotlinInt với operators
3. Implement KotlinString
4. Implement KotlinBoolean
5. Create CallFrame class
6. Create RuntimeEnvironment
7. Test all operations

**Test cases**:
```python
def test_kotlin_int_addition():
    x = KotlinInt(5)
    y = KotlinInt(10)
    result = x + y
    assert result.get_value() == 15
    assert result.get_type() == "Int"

def test_string_concatenation():
    s1 = KotlinString("Hello ")
    s2 = KotlinString("World")
    result = s1 + s2
    assert result.get_value() == "Hello World"
```

### Phase 4b: Evaluator (2 days)

**Files to create**:
- `src/interpreter/evaluator.py`
- `tests/test_interpreter.py`

**Implementation steps**:
1. Define ASTVisitor base class
2. Implement Evaluator với visitor pattern
3. Handle all node types
4. Support built-in functions
5. Test execution của complete programs

**Example test**:
```python
def test_simple_program():
    code = """
    fun main() {
        val x = 5
        val y = 10
        println(x + y)
    }
    """
    output = execute_kotlin_code(code)
    assert output == "15\n"
```

## 🎨 Visualization Implementation

### AST Visualization with Graphviz

**File**: `src/utils/visualizer.py`

```python
from graphviz import Digraph

class ASTVisualizer:
    def __init__(self):
        self.graph = Digraph()
        self.node_count = 0
    
    def visualize(self, ast: ASTNode, output_file: str = "ast"):
        self._visit(ast)
        self.graph.render(output_file, format='png', cleanup=True)
    
    def _visit(self, node: ASTNode, parent_id: str = None):
        node_id = f"node{self.node_count}"
        self.node_count += 1
        
        # Create node label
        label = self._get_node_label(node)
        self.graph.node(node_id, label)
        
        # Connect to parent
        if parent_id:
            self.graph.edge(parent_id, node_id)
        
        # Visit children
        for child in self._get_children(node):
            self._visit(child, node_id)
        
        return node_id
```

### Verbose Output Formatting

**File**: `src/utils/output_formatter.py`

```python
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

class OutputFormatter:
    def __init__(self, verbose: bool = False):
        self.console = Console()
        self.verbose = verbose
    
    def print_phase_header(self, phase_name: str):
        self.console.print(f"\n[bold cyan][PHASE] {phase_name}[/bold cyan]")
        self.console.print("─" * 60)
    
    def print_tokens(self, tokens: List[Token]):
        table = Table(title="Tokens")
        table.add_column("Index", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Value", style="yellow")
        table.add_column("Location", style="blue")
        
        for i, token in enumerate(tokens):
            table.add_row(
                str(i),
                token.type.name,
                token.value,
                f"{token.location.line}:{token.location.column}"
            )
        
        self.console.print(table)
    
    def print_symbol_table(self, scope_manager: ScopeManager):
        for i, scope in enumerate(scope_manager.scopes):
            table = Table(title=f"Scope {i}: {scope.scope_name}")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Mutable", style="yellow")
            
            for name, symbol in scope.symbols.items():
                table.add_row(
                    name,
                    symbol.type,
                    "Yes" if symbol.is_mutable else "No"
                )
            
            self.console.print(table)
```

## 🧪 Testing Strategy

### Unit Tests
- Test mỗi component riêng biệt
- Mock dependencies khi cần
- High coverage (aim for >90%)

### Integration Tests
- Test end-to-end execution
- Test error handling
- Test edge cases

### Test Organization
```
tests/
├── test_lexer.py          # Token generation tests
├── test_parser.py         # AST building tests
├── test_scope_management.py  # Symbol table tests
├── test_type_inference.py    # Type system tests
├── test_runtime_objects.py   # Runtime object tests
├── test_interpreter.py       # End-to-end tests
└── fixtures/
    ├── valid_programs/
    │   ├── hello_world.kt
    │   ├── functions.kt
    │   └── control_flow.kt
    └── invalid_programs/
        ├── type_error.kt
        └── undefined_var.kt
```

## 📦 Dependencies

**requirements.txt**:
```
# Core
dataclasses>=0.6
typing-extensions>=4.0

# Parsing (choose one)
ply>=3.11
# OR
lark-parser>=0.12

# Visualization
graphviz>=0.20
rich>=13.0
pygments>=2.14

# Testing
pytest>=7.0
pytest-cov>=4.0
hypothesis>=6.0
```

## 🚀 Main Entry Point

**File**: `main.py`

```python
import argparse
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.scope_manager import ScopeManager
from src.semantic.collection_pass import CollectionPhase
from src.semantic.type_checker_pass import TypeCheckingPhase
from src.interpreter.environment import RuntimeEnvironment
from src.interpreter.evaluator import Evaluator
from src.utils.error_collector import ErrorCollector
from src.utils.output_formatter import OutputFormatter
from src.utils.visualizer import ASTVisualizer

def main():
    parser = argparse.ArgumentParser(description='Kotlin Interpreter')
    parser.add_argument('file', help='Kotlin source file')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--visualize', action='store_true')
    parser.add_argument('-i', '--interactive', action='store_true')
    
    args = parser.parse_args()
    
    # Read source code
    with open(args.file, 'r') as f:
        source_code = f.read()
    
    formatter = OutputFormatter(args.verbose)
    
    # Phase 1: Lexing
    formatter.print_phase_header("LEXICAL ANALYSIS")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    if args.verbose:
        formatter.print_tokens(tokens)
    
    # Phase 2: Parsing
    formatter.print_phase_header("SYNTAX ANALYSIS")
    parser = Parser(tokens)
    ast = parser.parse()
    if args.visualize:
        visualizer = ASTVisualizer()
        visualizer.visualize(ast, "ast_output")
    
    # Phase 3: Semantic Analysis
    formatter.print_phase_header("SEMANTIC ANALYSIS")
    scope_manager = ScopeManager()
    error_collector = ErrorCollector()
    
    collector = CollectionPhase(scope_manager)
    collector.visit(ast)
    
    type_checker = TypeCheckingPhase(scope_manager, error_collector)
    type_checker.visit(ast)
    
    if error_collector.has_errors():
        error_collector.report_all()
        return 1
    
    if args.verbose:
        formatter.print_symbol_table(scope_manager)
    
    # Phase 4: Interpretation
    formatter.print_phase_header("EXECUTION")
    environment = RuntimeEnvironment()
    evaluator = Evaluator(environment)
    evaluator.visit(ast)
    
    return 0

if __name__ == '__main__':
    exit(main())
```

## ✅ Implementation Checklist

- [ ] Setup project structure
- [ ] Install dependencies
- [ ] Implement Phase 1: Lexer
- [ ] Write lexer tests
- [ ] Implement Phase 2: Parser
- [ ] Write parser tests
- [ ] Implement Phase 3a: Symbol Tables
- [ ] Write scope tests
- [ ] Implement Phase 3b: Type System
- [ ] Write type checking tests
- [ ] Implement Phase 4a: Runtime Objects
- [ ] Write runtime tests
- [ ] Implement Phase 4b: Evaluator
- [ ] Write interpreter tests
- [ ] Implement visualization tools
- [ ] Implement output formatting
- [ ] Create example programs
- [ ] Write documentation
- [ ] Final integration testing
- [ ] Prepare demo presentation
