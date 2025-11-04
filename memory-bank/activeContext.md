# Active Context - Kotlin Interpreter Demo Project

## 🎯 Current Project

**Project**: Kotlin Mini Compiler + Interpreter Demo  
**Purpose**: Mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z bằng Python  
**Status**: Planning Phase Complete ✅

## 📝 Project Summary

Đang xây dựng một educational demo về compiler/interpreter cho Kotlin, bao gồm:
- **Lexer**: Tokenization với location tracking
- **Parser**: Recursive descent parser tạo AST
- **Semantic Analyzer**: 2-pass analysis (Collection + Type Checking) với stack-based symbol tables
- **Interpreter**: Visitor-based evaluator với custom runtime objects

## 🔑 Key Technical Decisions

### 1. Stack-based Symbol Tables
- Mỗi scope có parent pointer
- Name resolution từ current scope lên parent
- Hỗ trợ nested scopes (functions, blocks, if/while)

### 2. Multi-Pass Semantic Analysis
- **Pass 1 (Collection)**: Thu thập function signatures
- **Pass 2 (Type Checking)**: Kiểm tra types với full context
- Cho phép forward references và type inference

### 3. Hybrid Runtime Model
- `KotlinObject` base class wrap Python types
- Retain Python performance
- Add Kotlin semantics layer
- Extensible cho future features

### 4. Error Collection System
- `ErrorCollector` pattern - không crash
- Collect tất cả errors
- Report với location info
- User-friendly messages

## 📦 Project Structure

```
kotlin_interpreter/
├── src/
│   ├── lexer/           # Tokenization
│   ├── parser/          # AST building
│   ├── semantic/        # Type checking, symbol tables
│   ├── interpreter/     # Execution engine
│   └── utils/           # Errors, visualizer, formatter
├── tests/               # Comprehensive test suite
├── examples/            # Kotlin sample programs
├── main.py             # Entry point
└── requirements.txt    # Dependencies
```

## 🎬 Demo Modes

1. **Verbose Mode** (`--verbose`): Chi tiết từng bước
2. **Quiet Mode** (default): Chỉ output/errors
3. **Interactive Mode** (`--interactive`): Step-through với inspection
4. **Visualize Mode** (`--visualize`): Tạo AST diagrams, execution traces

## 📚 Memory Bank Files

Đã tạo các file documentation:
1. ✅ `kotlin-interpreter-project.md` - Project overview, timeline
2. ✅ `kotlin-interpreter-architecture.md` - Technical architecture chi tiết
3. ✅ `kotlin-interpreter-implementation.md` - Implementation guide từng phase
4. ✅ `kotlin-interpreter-demo-modes.md` - UX design, demo modes

## 🎓 Key Insights từ Gemini 2.5 Feedback

### Về Scope Management
> "Bảng Ký hiệu của em không thể là một dict đơn giản. Em sẽ cần triển khai một Stack các Bảng Ký hiệu"

**Action**: Implemented stack-based SymbolTable với parent pointers

### Về Type Inference
> "val x = add(5, 3) đòi hỏi trình phân tích phải chạy sau khi nó đã xử lý khai báo của hàm add"

**Action**: Multi-pass analysis - Collection phase trước Type Checking phase

### Về Runtime Model
> "Một quyết định kỹ thuật quan trọng là: em sẽ dùng thẳng các kiểu của Python hay em sẽ tự định nghĩa các lớp đối tượng thời gian chạy"

**Action**: Hybrid approach - KotlinObject wrapping Python types

## ⏱️ Timeline & Progress

| Phase | Estimate | Status |
|-------|----------|--------|
| Planning & Design | 1 day | ✅ Complete |
| Phase 1: Lexer | 1-2 days | ⏳ Ready to start |
| Phase 2: Parser | 2-3 days | ⏳ Pending |
| Phase 3a: Symbol Tables | 2 days | ⏳ Pending |
| Phase 3b: Type System | 3 days | ⏳ Pending |
| Phase 4a: Runtime Model | 2 days | ⏳ Pending |
| Phase 4b: Evaluator | 2 days | ⏳ Pending |
| Testing & Integration | 2 days | ⏳ Pending |
| **Total** | **14-16 days** | |

## 🚀 Next Steps

1. **Setup project structure**: Tạo thư mục và files
2. **Install dependencies**: Setup requirements.txt và install
3. **Begin Phase 1**: Implement Lexer
   - Define Token types
   - Implement Lexer class
   - Write comprehensive tests
   - Add verbose output formatting

## 🎯 Success Criteria

- ✅ Parse và execute Kotlin programs cơ bản
- ✅ Hiển thị rõ từng phase của compilation
- ✅ Error messages chi tiết với location
- ✅ Visualizations educational và impressive
- ✅ Code quality cao, well-tested
- ✅ Demo flow professional

## 💡 Important Notes

### Kotlin Features Scope
**Must-have**:
- Functions, variables (val/var)
- Basic types (Int, String, Boolean)
- Expressions, operators
- Built-in functions (println)

**Should-have**:
- If/else, while loops
- Type inference
- String templates

**Nice-to-have**:
- Basic classes
- Null safety
- Lambda expressions

### Educational Focus
Demo này là educational tool, focus vào:
- ✅ Clarity over performance
- ✅ Step-by-step visualization
- ✅ Understanding compiler principles
- ✅ Clean, readable code với comments

### Tools & Libraries
- **ply** or **lark**: Parser generation
- **graphviz**: AST visualization
- **rich**: Terminal formatting
- **pytest**: Testing framework

## 📖 Related Context

**Previous Project**: Báo cáo LaTeX về Kotlin Programming Language Principles
- Đã có kiến thức về Kotlin từ "Kotlin in Action" và "The Joy of Kotlin"
- Context này complement báo cáo bằng practical implementation

**Learning Goals**:
1. Compiler construction principles
2. Type systems implementation
3. Runtime environment design
4. Error handling best practices
5. Educational software design

## 🔄 Update History

- **2025-01-04 23:58**: Created memory bank files, completed planning phase
- **2025-01-04 23:44**: Switched to ACT MODE, started creating memory bank
- **2025-01-04 23:16**: Received Gemini 2.5 feedback on technical architecture
- **2025-01-04 22:48**: Initial discussion about project goals and scope
