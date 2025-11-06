# Active Context - Kotlin Interpreter Demo Project

## 🎯 Current Project

**Project**: Kotlin Mini Compiler + Interpreter Demo  
**Purpose**: Mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z bằng Python  
**Status**: ✅ **HOÀN THÀNH & ĐANG CHẠY THÀNH CÔNG**

## 📝 Project Summary

Đã hoàn thành một educational demo về compiler/interpreter cho Kotlin, bao gồm:
- ✅ **Lexer**: Tokenization với location tracking
- ✅ **Parser**: Recursive descent parser tạo AST
- ✅ **Semantic Analyzer**: 2-pass analysis (Collection + Type Checking) với stack-based symbol tables
- ✅ **Interpreter**: Visitor-based evaluator với custom runtime objects
- ✅ **Demo A→Z**: Verbose output hiển thị từng bước compilation pipeline

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

## 🎓 Key Insights & Lessons Learned

### Từ Gemini 2.5 - Architecture Feedback

#### Về Scope Management
> "Bảng Ký hiệu của em không thể là một dict đơn giản. Em sẽ cần triển khai một Stack các Bảng Ký hiệu"

**Action**: ✅ Implemented stack-based SymbolTable với parent pointers

#### Về Type Inference
> "val x = add(5, 3) đòi hỏi trình phân tích phải chạy sau khi nó đã xử lý khai báo của hàm add"

**Action**: ✅ Multi-pass analysis - Collection phase trước Type Checking phase

#### Về Runtime Model
> "Một quyết định kỹ thuật quan trọng là: em sẽ dùng thẳng các kiểu của Python hay em sẽ tự định nghĩa các lớp đối tượng thời gian chạy"

**Action**: ✅ Hybrid approach - KotlinObject wrapping Python types

### Từ Gemini - Critical Bug Fix (Nov 6, 2025)

#### Python @dataclass Inheritance Pitfall
**Problem Discovered**:
```python
@dataclass
class Declaration(ASTNode):
    location: SourceLocation  # Parent field

@dataclass  
class FunctionDeclaration(Declaration):
    name: str
    parameters: List[Parameter]
    # Child classes KHÔNG NÊN redefine 'location'
    
# Python tạo: __init__(location, name, parameters, ...)
# NOT: __init__(name, parameters, ..., location)
```

**Root Cause**: 
- Python `@dataclass` với inheritance tự động đặt **parent fields FIRST** trong `__init__()`
- Child classes redefining `location` gây redundant và confusing
- Parser gọi với sai thứ tự parameters → TypeError

**Solution Applied**: ✅
- Sửa TẤT CẢ 15+ constructor calls trong `parser.py`
- Đặt `location` parameter ĐẦU TIÊN cho:
  - 2 Declarations (VariableDeclaration, FunctionDeclaration)
  - 6 Statements (Block, If, While, Return, Expression, Declaration)
  - 7 Expressions (Call, Binary, Unary, Assignment, Literal, Identifier, If)

**Lesson Learned**: 
- Khi dùng `@dataclass` với inheritance, HIỂU RÕ field ordering behavior
- Đọc Python docs về dataclass inheritance TRƯỚC KHI implement
- Nếu parent có fields, child's `__init__` sẽ nhận parent fields TRƯỚC

## ⏱️ Timeline & Progress

| Phase | Estimate | Actual | Status |
|-------|----------|--------|--------|
| Planning & Design | 1 day | 1 day | ✅ Complete |
| Phase 1: Lexer | 1-2 days | 1 day | ✅ Complete |
| Phase 2: Parser | 2-3 days | 2 days | ✅ Complete |
| Phase 3a: Symbol Tables | 2 days | 1 day | ✅ Complete |
| Phase 3b: Type System | 3 days | 2 days | ✅ Complete |
| Phase 4a: Runtime Model | 2 days | 1 day | ✅ Complete |
| Phase 4b: Evaluator | 2 days | 1 day | ✅ Complete |
| Testing & Debugging | 2 days | 1 day | ✅ Complete |
| Bug Fix (@dataclass) | - | 2 hours | ✅ Complete |
| **Total** | **14-16 days** | **~10 days** | ✅ **DONE** |

## ✅ Project Complete - Demo Running

**Current Status**: Interpreter đang chạy thành công!

**Test Command**:
```bash
cd kotlin_interpreter && python main.py examples/hello_world.kt
```

**Output Demo A→Z**:
```
[A] Soạn thảo (Writing) - ✓
[B] Phân tích Từ vựng (Lexical Analysis) - ✓ 21 tokens
[C] Phân tích Cú pháp (Syntax Analysis) - ✓ AST created
[D] Phân tích Ngữ nghĩa (Semantic Analysis) - ✓ Type checking passed
[E] Sinh mã (Code Generation) - ✓ Simplified (AST ready)
[F] Thực thi (Execution) - ✓ Output: 15
[Z] Kết quả (Result) - ✓ Program completed
```

**Next Step**: 🌐 **Streamlit Web GUI** (NEW FEATURE)
- Create web-based interactive visualizer
- Replace terminal-only output với browser GUI
- Step-by-step visualization với code editor
- Timeline: ~4 giờ implementation

**Future Enhancements**:
1. Add more Kotlin features (classes, lambdas, etc.)
2. Improve error messages
3. Add more test cases
4. Create additional demo programs
5. Document the codebase thoroughly

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

- **2025-11-07 00:09**: 📝 Planned Streamlit Web GUI - documented in `kotlin-interpreter-streamlit-gui.md`
- **2025-11-06 23:58**: ✅ Project COMPLETE - Demo chạy thành công từ A→Z
- **2025-11-06 23:51**: Fixed critical @dataclass inheritance bug với Gemini's help
- **2025-11-06**: Completed implementation của tất cả phases
- **2025-01-04 23:58**: Created memory bank files, completed planning phase
- **2025-01-04 23:44**: Switched to ACT MODE, started creating memory bank
- **2025-01-04 23:16**: Received Gemini 2.5 feedback on technical architecture
- **2025-01-04 22:48**: Initial discussion about project goals and scope
