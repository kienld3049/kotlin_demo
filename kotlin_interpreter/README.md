# Kotlin Mini Interpreter

Educational demo mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z bằng Python.

## 📚 Giới thiệu

Project này implement một mini compiler + interpreter cho Kotlin, bao gồm:

1. **Lexical Analysis** - Tokenization
2. **Syntax Analysis** - AST construction
3. **Semantic Analysis** - Type checking & symbol tables
4. **Execution** - Interpretation với runtime model

## 🎯 Mục tiêu

- ✅ Educational tool để hiểu compiler construction
- ✅ Visualize từng phase của compilation process
- ✅ Interactive exploration của AST, scopes, types
- ✅ Professional demo quality

## 🚀 Cài đặt

```bash
# Clone repository
cd kotlin_interpreter

# Cài đặt dependencies
pip install -r requirements.txt

# (Optional) Cài đặt graphviz cho visualization
# Ubuntu/Debian:
sudo apt-get install graphviz
# macOS:
brew install graphviz
```

## 💡 Sử dụng

### Basic Usage

```bash
# Chạy file Kotlin
python main.py examples/hello_world.kt

# Verbose mode - hiển thị chi tiết từng phase
python main.py examples/hello_world.kt --verbose

# Interactive mode - step through execution
python main.py examples/hello_world.kt --interactive

# Visualize mode - tạo AST diagrams
python main.py examples/hello_world.kt --visualize
```

### Demo Modes

1. **Quiet Mode** (default): Chỉ hiển thị output hoặc errors
2. **Verbose Mode** (`--verbose`): Chi tiết từng bước compilation
3. **Interactive Mode** (`--interactive`): Step-by-step với inspection
4. **Visualize Mode** (`--visualize`): Generate AST và execution diagrams

## 📖 Kotlin Features Support

### Must-have (Core)
- ✅ Functions với parameters
- ✅ Variables: `val` (immutable), `var` (mutable)
- ✅ Types: `Int`, `String`, `Boolean`
- ✅ Expressions và operators: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, etc.
- ✅ Built-in functions: `println()`

### Should-have
- ✅ Control flow: `if/else`, `while`
- ✅ Type inference
- ✅ String templates: `"Value is $x"`

### Nice-to-have (Future)
- ⏳ Basic classes
- ⏳ Null safety
- ⏳ Lambda expressions

## 🏗️ Architecture

```
kotlin_interpreter/
├── src/
│   ├── lexer/           # Tokenization
│   │   ├── token.py     # Token types & definitions
│   │   └── lexer.py     # Lexer implementation
│   ├── parser/          # AST construction
│   │   ├── ast_nodes.py # AST node classes
│   │   └── parser.py    # Recursive descent parser
│   ├── semantic/        # Type checking & analysis
│   │   ├── symbol_table.py      # Symbol management
│   │   ├── type_system.py       # Type definitions
│   │   ├── collection_pass.py   # Declaration collection
│   │   └── type_checker_pass.py # Type checking
│   ├── interpreter/     # Execution engine
│   │   ├── runtime_objects.py   # Kotlin object model
│   │   ├── environment.py       # Runtime environment
│   │   └── evaluator.py         # AST evaluator
│   └── utils/           # Utilities
│       ├── errors.py            # Error definitions
│       ├── error_collector.py   # Error collection
│       ├── visualizer.py        # AST visualization
│       └── output_formatter.py  # Pretty printing
├── tests/               # Test suite
├── examples/            # Kotlin example programs
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_lexer.py -v
```

## 📊 Example Output (Verbose Mode)

```
╔════════════════════════════════════════════════════════════╗
║         KOTLIN INTERPRETER - VERBOSE MODE                  ║
╚════════════════════════════════════════════════════════════╝

[PHASE 1] 🔤 LEXICAL ANALYSIS
────────────────────────────────────────────────────────────
✅ Lexer completed: 15 tokens generated

[PHASE 2] 🌳 SYNTAX ANALYSIS
────────────────────────────────────────────────────────────
✅ Parser completed: AST with 8 nodes

[PHASE 3] 🔍 SEMANTIC ANALYSIS
────────────────────────────────────────────────────────────
✅ Semantic analysis completed: No errors

[PHASE 4] 🚀 EXECUTION
────────────────────────────────────────────────────────────
╔════════════════════════════════════════════════════════════╗
║                    PROGRAM OUTPUT                          ║
╠════════════════════════════════════════════════════════════╣
║  Hello, World!                                             ║
╚════════════════════════════════════════════════════════════╝
```

## 🎓 Learning Resources

Xem thêm trong `memory-bank/`:
- `kotlin-interpreter-project.md` - Project overview
- `kotlin-interpreter-architecture.md` - Technical architecture
- `kotlin-interpreter-implementation.md` - Implementation guide
- `kotlin-interpreter-demo-modes.md` - Demo modes & UX

## 📝 License

Educational project - Free to use and modify

## 👨‍💻 Author

Created as part of Natural Language and Natural Language Learning Theory course project.
