# Kotlin Mini Interpreter

Educational demo mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z bằng Python.

## 📚 Giới thiệu

Project này implement một mini compiler + interpreter cho Kotlin, bao gồm:

1. **Lexical Analysis** - Tokenization
2. **Syntax Analysis** - AST construction
3. **Semantic Analysis** - Type checking & symbol tables
4. **IR Generation** - Intermediate representation ✨ NEW
5. **Code Generation** - Multi-platform code generation ✨ NEW
6. **Execution** - Interpretation với runtime model

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

### Web GUI (Recommended)

```bash
# Khởi động Streamlit web interface
streamlit run streamlit_app.py
# hoặc
python -m streamlit run streamlit_app.py

# Mở browser tại http://localhost:8501
```

**Tính năng Web GUI:**
- 🎨 Interactive code editor
- 📊 Visualize toàn bộ 6 phases của compilation
- 🔧 Xem IR instructions
- 🎯 Xem generated code cho JVM/JavaScript/Native
- 📈 Symbol table và AST visualization
- 🧪 Built-in example programs

### CLI Usage

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
│   │   └── errors.py            # Semantic errors
│   ├── ir/              # ✨ Intermediate Representation
│   │   ├── ir_nodes.py          # IR instruction types
│   │   └── ir_generator.py      # AST → IR transformer
│   ├── codegen/         # ✨ Code Generation
│   │   └── generators.py        # JVM/JS/Native generators
│   ├── runtime/         # Execution engine
│   │   ├── runtime_objects.py   # Kotlin object model
│   │   ├── environment.py       # Runtime environment
│   │   └── evaluator.py         # AST evaluator
│   └── gui/             # Web GUI components
│       └── state_manager.py     # Streamlit state management
├── docs/                # Documentation
│   ├── ir_and_codegen_guide.md  # IR & CodeGen guide
│   ├── interview_prep.md        # Interview preparation
│   └── presentation_script.md   # Presentation script
├── tests/               # Test suite
├── examples/            # Kotlin example programs
├── main.py             # CLI entry point
├── streamlit_app.py    # Web GUI entry point
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

[PHASE 4] 🔧 IR GENERATION ✨ NEW
────────────────────────────────────────────────────────────
✅ IR generated: 5 instructions

[PHASE 5] 🎯 CODE GENERATION ✨ NEW
────────────────────────────────────────────────────────────
✅ JVM bytecode: 45 lines
✅ JavaScript: 5 lines
✅ Native assembly: 35 lines

[PHASE 6] 🚀 EXECUTION
────────────────────────────────────────────────────────────
╔════════════════════════════════════════════════════════════╗
║                    PROGRAM OUTPUT                          ║
╠════════════════════════════════════════════════════════════╣
║  Hello, World!                                             ║
╚════════════════════════════════════════════════════════════╝
```

## 🎯 New Features: IR & Code Generation

### IR Generation
Chuyển đổi AST thành platform-independent intermediate representation:
- Simple 3-address code format
- Easy to optimize và transform
- Foundation cho multi-platform code generation

**Example IR:**
```
1. a = 10
2. b = 20
3. temp0 = a + b
4. c = temp0
5. call println(c)
```

### Code Generation
Sinh mã cho 3 nền tảng từ IR:

1. **JVM Bytecode** (Jasmin format)
   - Stack-based virtual machine
   - Educational simulation of JVM instructions

2. **JavaScript**
   - Functional code có thể chạy trong browser/Node.js
   - Register-based execution model

3. **Native Assembly** (x86-64)
   - Pseudo assembly code
   - Direct CPU register manipulation

Xem thêm: `docs/ir_and_codegen_guide.md`

## 🎓 Learning Resources

**Documentation:**
- `docs/ir_and_codegen_guide.md` - IR & Code Generation guide
- `docs/interview_prep.md` - Interview preparation guide
- `docs/presentation_script.md` - Presentation script

**Memory Bank:**
- `memory-bank/kotlin-interpreter-project.md` - Project overview
- `memory-bank/kotlin-interpreter-architecture.md` - Technical architecture
- `memory-bank/kotlin-interpreter-implementation.md` - Implementation guide
- `memory-bank/kotlin-interpreter-streamlit-gui.md` - GUI implementation

## 📝 License

Educational project - Free to use and modify

## 👨‍💻 Author

Created as part of Natural Language and Natural Language Learning Theory course project.
