# IR Generation & Code Generation Guide

## Tổng quan

Đã thêm 2 bước mới vào Kotlin Interpreter pipeline:
- **Bước 4: IR Generation** - Tạo mã trung gian (Intermediate Representation)
- **Bước 5: Code Generation** - Sinh mã cho các nền tảng khác nhau

## Pipeline đầy đủ (6 bước)

```
Source Code
    ↓
1. Lexical Analysis (Tokenization)
    ↓
2. Syntax Analysis (Parsing → AST)
    ↓
3. Semantic Analysis (Type checking, Symbol Table)
    ↓
4. IR Generation (AST → IR) ← MỚI
    ↓
5. Code Generation (IR → Target Code) ← MỚI
    ↓
6. Execution (Interpret or Run Generated Code)
```

## Bước 4: IR Generation

### Mục đích
- Chuyển đổi AST thành dạng mã trung gian độc lập với nền tảng
- IR đơn giản hóa quá trình sinh mã cho nhiều nền tảng khác nhau

### IR Instructions

IR bao gồm các loại instruction cơ bản:

1. **IRAssignment**: Gán giá trị cho biến
   ```
   x = 10
   ```

2. **IRBinaryOp**: Phép toán hai ngôi
   ```
   temp0 = a + b
   ```

3. **IRFunctionCall**: Gọi hàm
   ```
   call println(x)
   ```

### Ví dụ

**Kotlin Code:**
```kotlin
fun main() {
    val a = 10
    val b = 20
    val c = a + b
    println(c)
}
```

**Generated IR:**
```
1. a = 10
2. b = 20
3. temp0 = a + b
4. c = temp0
5. call println(c)
```

## Bước 5: Code Generation

### Mục đích
- Từ IR, sinh mã cho các nền tảng cụ thể
- Hỗ trợ 3 targets: JVM, JavaScript, Native

### 1. JVM Bytecode Generator

Sinh mã bytecode cho Java Virtual Machine (Jasmin format).

**Ví dụ output:**
```jasmin
;; JVM Bytecode (Simplified Simulation)
.class public Main
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
  .limit stack 10
  .limit locals 10

  bipush 10  ; push constant 10
  istore 1   ; store to a

  bipush 20
  istore 2   ; store to b

  iload 1    ; load a
  iload 2    ; load b
  iadd       ; perform +
  istore 3   ; store to temp0

  ; Call println
  getstatic java/lang/System/out Ljava/io/PrintStream;
  iload 3
  invokevirtual java/io/PrintStream/println(I)V

  return
.end method
```

### 2. JavaScript Generator

Sinh mã JavaScript có thể chạy trong browser hoặc Node.js.

**Ví dụ output:**
```javascript
// JavaScript (Generated from IR)
let a = 10;
let b = 20;
let temp0 = a + b;
let c = temp0;
console.log(c);
```

### 3. Native Code Generator

Sinh mã assembly x86-64 (pseudo code cho mục đích educational).

**Ví dụ output:**
```asm
; Native Assembly (Pseudo Code)
section .data
  a: dq 0
  b: dq 0
  temp0: dq 0
  c: dq 0

section .text
global main

main:
  ; Assign a = 10
  mov rax, 10
  mov [a], rax

  ; Assign b = 20
  mov rax, 20
  mov [b], rax

  ; Compute: temp0 = a + b
  mov rax, [a]
  add rax, [b]
  mov [temp0], rax

  ; Assign c = temp0
  mov rax, [temp0]
  mov [c], rax

  ; Call println
  mov rdi, [c]
  call printf

  ; Exit program
  mov rax, 60
  xor rdi, rdi
  syscall
```

## Sử dụng trong GUI

### Hiển thị IR

1. Chạy chương trình Kotlin
2. Bật checkbox "Hiển thị IR" trong sidebar
3. Xem IR instructions ở Bước 4

### Hiển thị Code Generation

1. Chạy chương trình Kotlin
2. Bật checkbox "Hiển thị Code Generation" trong sidebar
3. Xem generated code ở Bước 5
4. Chuyển đổi giữa 3 tabs:
   - ☕ JVM Bytecode
   - 🟨 JavaScript
   - ⚙️ Native Assembly

## Kiến trúc Code

### Module Structure

```
src/
├── ir/
│   ├── __init__.py
│   ├── ir_nodes.py      # IR data structures
│   └── ir_generator.py  # AST → IR transformer
│
└── codegen/
    ├── __init__.py
    └── generators.py    # Target code generators
```

### Luồng dữ liệu

```
AST (from Parser)
    ↓
IRGenerator.generate()
    ↓
List[IRNode] (IR instructions)
    ↓
├── JVMBytecodeGenerator.generate() → JVM bytecode
├── JavaScriptGenerator.generate()   → JavaScript
└── NativeCodeGenerator.generate()   → Assembly
```

## Testing

Test với các chương trình mẫu:

1. **Hello World** - Test cơ bản
2. **Variables** - Test assignment và arithmetic
3. **Functions** - Test function calls
4. **If Expression** - Test control flow
5. **While Loop** - Test loops

Mỗi chương trình sẽ hiển thị đầy đủ 6 bước trong pipeline.

## Lưu ý

- IR và Code Generation là **educational simulations**
- JVM bytecode sử dụng Jasmin format (không phải bytecode thật)
- Native assembly là pseudo code x86-64
- JavaScript generator là functional và có thể chạy thực tế
- Các generator đơn giản hóa để dễ hiểu, không phải production-ready

## Tài liệu tham khảo

- JVM Specification: https://docs.oracle.com/javase/specs/jvms/se8/html/
- Jasmin Assembler: http://jasmin.sourceforge.net/
- x86-64 Assembly: https://www.cs.cmu.edu/~fp/courses/15213-s07/misc/asm64-handout.pdf
