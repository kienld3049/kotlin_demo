# Kotlin Interpreter Demo Project

## 🎯 Mục tiêu Dự án

Xây dựng một **Kotlin Mini Compiler + Interpreter** hoàn chỉnh bằng Python để mô phỏng quá trình biên dịch và thực thi code Kotlin từ A đến Z.

## 📊 Tổng quan

### Mục đích
- **Demo giáo dục**: Minh họa các giai đoạn của compiler/interpreter
- **Hiểu sâu về PL**: Áp dụng các nguyên lý Programming Language Principles
- **Visualization**: Hiển thị từng bước xử lý code một cách trực quan

### Phạm vi
Hỗ trợ subset của Kotlin bao gồm:
- **Must-have**: Functions, variables (val/var), basic types (Int, String, Boolean), expressions, println
- **Should-have**: If/else, while loops, type inference, string templates
- **Nice-to-have**: Basic classes, null safety, lambdas

## 🏗️ Kiến trúc 4 Phases

### Phase 1: Lexer (Tokenizer)
- **Input**: Raw Kotlin source code (String)
- **Output**: List of Tokens
- **Chức năng**: Phân tích từ vựng, tạo tokens với location info
- **Thời gian**: 1-2 ngày

### Phase 2: Parser (Syntax Analyzer)
- **Input**: List of Tokens
- **Output**: Abstract Syntax Tree (AST)
- **Chức năng**: Xây dựng cây cú pháp theo grammar Kotlin
- **Thời gian**: 2-3 ngày

### Phase 3: Semantic Analyzer
- **Input**: AST
- **Output**: Validated + Type-annotated AST
- **Chức năng**: 
  - **Pass 1**: Collection - Thu thập declarations
  - **Pass 2**: Type Checking - Kiểm tra kiểu, infer types
  - Symbol table management (Stack-based scopes)
- **Thời gian**: 4-5 ngày (phức tạp nhất)

### Phase 4: Interpreter
- **Input**: Validated AST
- **Output**: Program execution + output
- **Chức năng**: 
  - Visitor-based AST traversal
  - Runtime environment with call frames
  - Execute Kotlin code directly
- **Thời gian**: 3-4 ngày

## 🎬 Demo Modes

### 1. Verbose Mode (`--verbose`)
Hiển thị chi tiết từng bước:
- Token list với line/column info
- AST construction step-by-step
- Symbol table changes
- Execution trace với variable states

### 2. Quiet Mode (default)
Chỉ hiển thị output cuối cùng hoặc errors

### 3. Interactive Mode (`--interactive`)
Cho phép:
- Pause sau mỗi phase
- Inspect symbol table
- Step through execution
- Commands: next, continue, skip, inspect

### 4. Visualize Mode (`--visualize`)
Tạo visualizations:
- AST tree diagrams (PNG/SVG)
- Call stack diagrams
- Scope hierarchy
- Execution flow animation

## 📦 Tech Stack

### Core Libraries
- **ply** hoặc **lark-parser**: Lexer/Parser generation
- **dataclasses**: AST node definitions
- **typing**: Type hints

### Visualization
- **graphviz**: AST visualization
- **rich**: Terminal pretty printing
- **pygments**: Syntax highlighting

### Testing
- **pytest**: Unit testing
- **hypothesis**: Property-based testing

## 📁 Cấu trúc Thư mục

```
kotlin_interpreter/
├── src/
│   ├── lexer/
│   │   ├── token.py
│   │   └── lexer.py
│   ├── parser/
│   │   ├── ast_nodes.py
│   │   └── parser.py
│   ├── semantic/
│   │   ├── symbol_table.py
│   │   ├── scope_manager.py
│   │   ├── type_system.py
│   │   ├── collection_pass.py
│   │   └── type_checker_pass.py
│   ├── interpreter/
│   │   ├── runtime_objects.py
│   │   ├── environment.py
│   │   └── evaluator.py
│   └── utils/
│       ├── errors.py
│       ├── error_collector.py
│       └── visualizer.py
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   └── test_interpreter.py
├── examples/
│   ├── hello_world.kt
│   ├── variables.kt
│   ├── functions.kt
│   └── control_flow.kt
├── main.py
├── requirements.txt
└── README.md
```

## ⏱️ Timeline

| Phase | Thời gian | Status |
|-------|-----------|--------|
| Phase 1: Lexer | 1-2 ngày | ⏳ Pending |
| Phase 2: Parser | 2-3 ngày | ⏳ Pending |
| Phase 3a: Symbol Tables | 2 ngày | ⏳ Pending |
| Phase 3b: Type System | 3 ngày | ⏳ Pending |
| Phase 4a: Runtime Model | 2 ngày | ⏳ Pending |
| Phase 4b: Evaluator | 2 ngày | ⏳ Pending |
| Testing & Integration | 2 ngày | ⏳ Pending |
| **Tổng cộng** | **14-16 ngày** | |

## 🎓 Learning Outcomes

Sau khi hoàn thành project này, sẽ hiểu rõ:
1. **Lexical Analysis**: Tokenization, regular expressions
2. **Syntax Analysis**: CFG, recursive descent parsing, AST
3. **Semantic Analysis**: Symbol tables, type systems, scope management
4. **Interpretation**: Runtime environments, visitor pattern, execution models
5. **Error Handling**: Compiler error design, user-friendly messages
6. **Software Architecture**: Clean separation of concerns, design patterns

## 📚 Tài liệu Tham khảo

### Books
- "Crafting Interpreters" - Robert Nystrom
- "Modern Compiler Implementation" - Andrew Appel
- "Language Implementation Patterns" - Terence Parr

### Online Resources
- Kotlin Language Specification
- Python ply/lark documentation
- Compiler construction courses (Stanford CS143, MIT 6.035)

## ✅ Success Criteria

1. ✅ Có thể parse và execute Kotlin programs cơ bản
2. ✅ Hiển thị rõ ràng từng phase của compilation
3. ✅ Error messages chi tiết với line/column info
4. ✅ Visualizations dễ hiểu cho educational purposes
5. ✅ Code quality cao, well-tested, documented
6. ✅ Demo flow mượt mà, impressive

## 🚀 Next Steps

1. Bắt đầu với Phase 1: Lexer
2. Implement incrementally với TDD
3. Validate sau mỗi phase trước khi tiếp tục
4. Integrate visualizations sớm để demo được ngay
