# Kotlin Interpreter - Technical Architecture

## 🏛️ System Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         Kotlin Source Code (.kt)                │
│     fun main() { println("Hello World") }       │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│  1. LEXER (Tokenizer)                           │
│  Input: String → Output: List[Token]            │
│  ["fun", "main", "(", ")", "{", ...]            │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│  2. PARSER (Syntax Analyzer)                    │
│  Input: Tokens → Output: AST                    │
│  Abstract Syntax Tree                           │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│  3. SEMANTIC ANALYZER (2-Pass)                  │
│  Pass 1: Collection Phase                       │
│  Pass 2: Type Checking Phase                    │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│  4. INTERPRETER (Evaluator)                     │
│  Direct execution via AST traversal             │
└────────────────┬────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────┐
│         OUTPUT: "Hello World"                   │
└─────────────────────────────────────────────────┘
```

## 📦 Component Specifications

### 1. Lexer (Tokenizer)

#### Token Types
```python
class TokenType(Enum):
    # Keywords
    FUN = "fun"
    VAL = "val"
    VAR = "var"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    
    # Identifiers & Literals
    IDENTIFIER = "identifier"
    INT_LITERAL = "int_literal"
    STRING_LITERAL = "string_literal"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    ASSIGN = "="
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    DOT = "."
    
    # Special
    EOF = "eof"
    NEWLINE = "newline"
```

#### Token Class
```python
@dataclass
class Token:
    type: TokenType
    value: str
    location: SourceLocation
    
@dataclass
class SourceLocation:
    line: int
    column: int
    file: str = "unknown"
```

#### Lexer Algorithm
1. Read source code character by character
2. Skip whitespace (except newlines for Kotlin)
3. Identify keywords, identifiers, literals, operators
4. Track line/column for each token
5. Collect errors without crashing

### 2. Parser (AST Builder)

#### Grammar (Simplified BNF)
```
program        → declaration* EOF
declaration    → functionDecl | statement

functionDecl   → "fun" IDENTIFIER "(" parameters? ")" (":" type)? block
parameters     → parameter ("," parameter)*
parameter      → IDENTIFIER ":" type

block          → "{" statement* "}"
statement      → valDecl | varDecl | exprStmt | returnStmt | ifStmt | whileStmt
valDecl        → "val" IDENTIFIER (":" type)? "=" expression
varDecl        → "var" IDENTIFIER (":" type)? "=" expression
exprStmt       → expression
returnStmt     → "return" expression?
ifStmt         → "if" "(" expression ")" block ("else" block)?
whileStmt      → "while" "(" expression ")" block

expression     → assignment
assignment     → IDENTIFIER "=" assignment | logicalOr
logicalOr      → logicalAnd ("||" logicalAnd)*
logicalAnd     → equality ("&&" equality)*
equality       → comparison (("==" | "!=") comparison)*
comparison     → term (("<" | ">" | "<=" | ">=") term)*
term           → factor (("+" | "-") factor)*
factor         → unary (("*" | "/") unary)*
unary          → ("!" | "-") unary | call
call           → primary ("(" arguments? ")")*
primary        → literal | IDENTIFIER | "(" expression ")"

literal        → INT_LITERAL | STRING_LITERAL | "true" | "false"
type           → "Int" | "String" | "Boolean" | "Unit"
```

#### AST Node Hierarchy
```python
# Base class
class ASTNode:
    location: SourceLocation

# Declarations
class FunctionDecl(ASTNode):
    name: str
    parameters: List[Parameter]
    return_type: Optional[str]
    body: BlockStatement

class Parameter(ASTNode):
    name: str
    type: str

# Statements
class Statement(ASTNode):
    pass

class BlockStatement(Statement):
    statements: List[Statement]

class ValDecl(Statement):
    name: str
    declared_type: Optional[str]
    initializer: Expression
    inferred_type: Optional[str] = None

class VarDecl(Statement):
    name: str
    declared_type: Optional[str]
    initializer: Expression
    inferred_type: Optional[str] = None

class ExpressionStatement(Statement):
    expression: Expression

class ReturnStatement(Statement):
    value: Optional[Expression]

class IfStatement(Statement):
    condition: Expression
    then_block: BlockStatement
    else_block: Optional[BlockStatement]

class WhileStatement(Statement):
    condition: Expression
    body: BlockStatement

# Expressions
class Expression(ASTNode):
    pass

class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression

class UnaryExpression(Expression):
    operator: TokenType
    operand: Expression

class FunctionCall(Expression):
    callee: str
    arguments: List[Expression]

class Identifier(Expression):
    name: str

class Literal(Expression):
    value: Any
    type: str  # "Int", "String", "Boolean"
```

### 3. Semantic Analyzer

#### 3.1 Symbol Table (Stack-based Scopes)

```python
class Symbol:
    """Represents a symbol in the symbol table"""
    def __init__(self, name: str, type: str, is_mutable: bool, location: SourceLocation):
        self.name = name
        self.type = type
        self.is_mutable = is_mutable
        self.location = location

class SymbolTable:
    """Single scope's symbol table"""
    def __init__(self, parent: Optional['SymbolTable'] = None, scope_name: str = ""):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent
        self.scope_name = scope_name
    
    def define(self, symbol: Symbol) -> None:
        if symbol.name in self.symbols:
            raise RedefinitionError(...)
        self.symbols[symbol.name] = symbol
    
    def resolve(self, name: str) -> Optional[Symbol]:
        # Tìm trong scope hiện tại
        if name in self.symbols:
            return self.symbols[name]
        # Tìm trong parent scopes
        if self.parent:
            return self.parent.resolve(name)
        return None

class ScopeManager:
    """Quản lý stack của symbol tables"""
    def __init__(self):
        self.scopes: List[SymbolTable] = []
        self.push_scope("global")
    
    def push_scope(self, name: str = ""):
        parent = self.scopes[-1] if self.scopes else None
        self.scopes.append(SymbolTable(parent, name))
    
    def pop_scope(self):
        self.scopes.pop()
    
    def current_scope(self) -> SymbolTable:
        return self.scopes[-1]
```

#### 3.2 Multi-Pass Analysis

**Pass 1: Collection Phase**
```python
class CollectionPhase(ASTVisitor):
    """Thu thập tất cả function declarations"""
    def __init__(self, scope_manager: ScopeManager):
        self.scope_manager = scope_manager
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        # Collect function signature
        func_symbol = Symbol(
            name=node.name,
            type=f"({', '.join(p.type for p in node.parameters)}) -> {node.return_type or 'Unit'}",
            is_mutable=False,
            location=node.location
        )
        self.scope_manager.current_scope().define(func_symbol)
        
        # Don't analyze body yet, just collect signature
```

**Pass 2: Type Checking Phase**
```python
class TypeCheckingPhase(ASTVisitor):
    """Kiểm tra kiểu và infer types"""
    def __init__(self, scope_manager: ScopeManager, error_collector: ErrorCollector):
        self.scope_manager = scope_manager
        self.error_collector = error_collector
    
    def visit_ValDecl(self, node: ValDecl):
        # Infer type from initializer
        expr_type = self.infer_type(node.initializer)
        
        if node.declared_type:
            # Check if matches declared type
            if expr_type != node.declared_type:
                self.error_collector.add_error(
                    TypeMismatchError(node.declared_type, expr_type, node.location)
                )
        else:
            # Infer type
            node.inferred_type = expr_type
        
        # Add to symbol table
        symbol = Symbol(
            name=node.name,
            type=node.declared_type or node.inferred_type,
            is_mutable=False,
            location=node.location
        )
        self.scope_manager.current_scope().define(symbol)
    
    def infer_type(self, expr: Expression) -> str:
        if isinstance(expr, Literal):
            return expr.type
        elif isinstance(expr, Identifier):
            symbol = self.scope_manager.current_scope().resolve(expr.name)
            if not symbol:
                self.error_collector.add_error(
                    UndefinedVariableError(expr.name, expr.location)
                )
                return "Error"
            return symbol.type
        elif isinstance(expr, BinaryExpression):
            left_type = self.infer_type(expr.left)
            right_type = self.infer_type(expr.right)
            return self.check_binary_op(expr.operator, left_type, right_type)
        elif isinstance(expr, FunctionCall):
            return self.check_function_call(expr)
        # ... more cases
```

### 4. Interpreter (Evaluator)

#### Runtime Object Model
```python
class KotlinObject:
    """Base class cho mọi runtime values"""
    def __init__(self, value: Any, type_name: str):
        self._value = value
        self._type = type_name
    
    def get_value(self):
        return self._value
    
    def get_type(self):
        return self._type

class KotlinInt(KotlinObject):
    def __init__(self, value: int):
        super().__init__(value, "Int")
    
    def __add__(self, other):
        if not isinstance(other, KotlinInt):
            raise TypeError(f"Cannot add Int and {other.get_type()}")
        return KotlinInt(self._value + other._value)
    
    def __sub__(self, other):
        # Similar...
    # ... other operations

class KotlinString(KotlinObject):
    def __init__(self, value: str):
        super().__init__(value, "String")
    
    def __add__(self, other):
        # String concatenation
        return KotlinString(self._value + str(other._value))

class KotlinBoolean(KotlinObject):
    def __init__(self, value: bool):
        super().__init__(value, "Boolean")
```

#### Runtime Environment
```python
class CallFrame:
    """Một frame trong call stack"""
    def __init__(self, function_name: str):
        self.function_name = function_name
        self.variables: Dict[str, KotlinObject] = {}

class RuntimeEnvironment:
    """Runtime execution environment"""
    def __init__(self):
        self.frames: List[CallFrame] = []
        self.push_frame("global")
        self.load_builtins()
    
    def push_frame(self, function_name: str):
        self.frames.append(CallFrame(function_name))
    
    def pop_frame(self):
        self.frames.pop()
    
    def set_variable(self, name: str, value: KotlinObject):
        self.frames[-1].variables[name] = value
    
    def get_variable(self, name: str) -> KotlinObject:
        # Search from current frame up
        for frame in reversed(self.frames):
            if name in frame.variables:
                return frame.variables[name]
        raise NameError(f"Undefined variable: {name}")
    
    def load_builtins(self):
        """Load built-in functions"""
        # println is special - handled in evaluator
        pass
```

#### Evaluator (Visitor Pattern)
```python
class Evaluator(ASTVisitor):
    """Execute AST via visitor pattern"""
    def __init__(self, environment: RuntimeEnvironment):
        self.environment = environment
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        # Store function for later calls
        # (simplified - actual impl more complex)
        pass
    
    def visit_ValDecl(self, node: ValDecl):
        value = self.evaluate(node.initializer)
        self.environment.set_variable(node.name, value)
    
    def visit_BinaryExpression(self, node: BinaryExpression) -> KotlinObject:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        if node.operator == TokenType.PLUS:
            return left + right  # Calls __add__
        elif node.operator == TokenType.MINUS:
            return left - right
        # ... other operators
    
    def visit_FunctionCall(self, node: FunctionCall) -> KotlinObject:
        if node.callee == "println":
            # Built-in function
            args = [self.evaluate(arg) for arg in node.arguments]
            print(args[0].get_value())
            return KotlinObject(None, "Unit")
        # ... handle user-defined functions
    
    def visit_Literal(self, node: Literal) -> KotlinObject:
        if node.type == "Int":
            return KotlinInt(int(node.value))
        elif node.type == "String":
            return KotlinString(node.value)
        elif node.type == "Boolean":
            return KotlinBoolean(node.value == "true")
```

## 🔄 Complete Execution Flow

```python
def execute_kotlin_code(source_code: str, verbose: bool = False):
    """Main entry point"""
    
    # Phase 1: Lexing
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    if verbose:
        print_tokens(tokens)
    
    # Phase 2: Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    if verbose:
        print_ast(ast)
        visualize_ast(ast)
    
    # Phase 3: Semantic Analysis
    scope_manager = ScopeManager()
    error_collector = ErrorCollector()
    
    # Pass 1: Collection
    collector = CollectionPhase(scope_manager)
    collector.visit(ast)
    
    # Pass 2: Type Checking
    type_checker = TypeCheckingPhase(scope_manager, error_collector)
    type_checker.visit(ast)
    
    if error_collector.has_errors():
        error_collector.report_all()
        return
    
    if verbose:
        print_symbol_table(scope_manager)
    
    # Phase 4: Interpretation
    environment = RuntimeEnvironment()
    evaluator = Evaluator(environment)
    evaluator.visit(ast)
```

## 🎯 Key Design Decisions

1. **Stack-based Symbol Tables**: Để handle nested scopes correctly
2. **Multi-pass Semantic Analysis**: Cho phép forward references và type inference
3. **Hybrid Runtime Model**: KotlinObject wrapping Python types để có flexibility
4. **Visitor Pattern**: Clean separation, easy to extend
5. **Error Collection**: Don't crash, collect all errors để user experience tốt hơn
6. **Incremental Development**: Mỗi phase độc lập, test được riêng
