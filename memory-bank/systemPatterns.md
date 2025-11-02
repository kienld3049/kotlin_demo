# System Patterns: Cấu trúc Báo cáo 12 Chương

## Kiến trúc tổng thể
Báo cáo được thiết kế theo mô hình **3 phần**:
1. **PHẦN I: Cơ sở lý thuyết** (Ch 1-4): Theory foundation
2. **PHẦN II: Paradigms & Features** (Ch 5-9): Core language features
3. **PHẦN III: Advanced & Practical** (Ch 10-12): Advanced topics và real-world

Distribution:
- **Theory-heavy** (từ Joy of Kotlin): Chapters 2, 5, 7, 8 (~33%)
- **Practice-heavy** (từ Kotlin in Action): Chapters 1, 10, 11, 12 (~33%)
- **Balanced** (cả 2 sách): Chapters 3, 4, 6, 9 (~33%)

## Detailed Chapter Structure

## PHẦN I: CƠ SỞ LÝ THUYẾT (Chapters 1-4)

### CHƯƠNG 1: GIỚI THIỆU VỀ KOTLIN
**Mục đích**: Set context và position của Kotlin

**Nội dung**:
- History & motivation (JetBrains story, Java pain points)
- Design goals: Pragmatic, Concise, Safe, Interoperable
- Position trong PL landscape (vs Java, Scala, Swift)
- Scope của báo cáo

**Sources**:
- Kotlin in Action: Preface, Ch 1 (Kotlin: what and why)
- Joy of Kotlin: Preface (Why Kotlin matters)

**Tone**: Practice-heavy, introductory

---

### CHƯƠNG 2: TRIẾT LÝ THIẾT KẾ
**Mục đích**: Establish design philosophy

**Nội dung**:
- Safe Programming philosophy (từ Joy of Kotlin)
- Pragmatic approach vs Academic purity
- Trade-offs: Theory vs Practice
- Design principles: Minimizing errors, Maximizing expressiveness

**Sources**:
- Joy of Kotlin: About this book (7 key techniques)
- Kotlin in Action: Ch 1 (Design goals)

**Key Concepts**:
- Referential transparency
- Abstraction over implementation
- Safe vs Unsafe operations

**Tone**: Theory-heavy

---

### CHƯƠNG 3: HỆ THỐNG KIỂU CƠ BẢN
**Mục đích**: Core type system

**Nội dung**:
- Static typing + Type inference
- Properties vs Fields
- Smart casts & Data-flow analysis
- Platform types

**Sources**:
- Kotlin in Action: Ch 2 (Basics), Ch 4 (Classes)
- Joy of Kotlin: "Using the right types"

**Tone**: Balanced

---

### CHƯƠNG 4: NULL SAFETY
**Mục đích**: Solving the billion-dollar mistake

**Nội dung**:
- Nullable types (T vs T?)
- Safe call (?.), Elvis (?:), Not-null assertion (!!)
- Compiler enforcement
- So sánh với Optional/Maybe/Option

**Sources**:
- Kotlin in Action: Ch 6 (Working with nullable values)
- Joy of Kotlin: Ch 6 (Optional data)

**Key Innovation**: 
- Null safety baked into type system (không phải wrapper)

**Tone**: Balanced

## PHẦN II: PARADIGMS & FEATURES (Chapters 5-9)

### CHƯƠNG 5: LẬP TRÌNH HÀM TRONG KOTLIN
**Mục đích**: FP support trong Kotlin

**Nội dung**:
- Pure functions & Referential transparency
- Higher-order functions
- Lambdas & Function types
- Currying & Partial application

**Sources**:
- Kotlin in Action: Ch 5 (Lambdas), Ch 10 (Higher-order functions)
- Joy of Kotlin: Ch 5 (Functions, Lists), "Abstracting common patterns"

**Key Concepts**:
- Functions as first-class values
- Function composition
- Point-free style

**Tone**: Theory-heavy

---

### CHƯƠNG 6: BẤT BIẾN & QUẢN LÝ TRẠNG THÁI
**Mục đích**: Immutability và state management

**Nội dung**:
- val vs var
- Data classes
- Immutability benefits (thread-safety, reasoning)
- Copy-on-write patterns
- Persistent data structures

**Sources**:
- Kotlin in Action: Ch 4 (Classes), Ch 7 (Operator overloading)
- Joy of Kotlin: "Favoring immutability", Ch 5 (Data sharing)

**Tone**: Balanced

---

### CHƯƠNG 7: XỬ LÝ LỖI AN TOÀN
**Mục đích**: Safe error handling

**Nội dung**:
- Problems với null & exceptions
- Option/Result types
- Partial vs Total functions
- Railway-oriented programming
- So sánh: Exceptions vs Functional error handling

**Sources**:
- Joy of Kotlin: Ch 7 (Handling errors, Optional data)
- Kotlin in Action: Ch 6 (Nullable types)

**Tone**: Theory-heavy

---

### CHƯƠNG 8: ĐỆ QUY & LAZINESS
**Mục đích**: Recursion và lazy evaluation

**Nội dung**:
- Tail recursion optimization (tailrec)
- Folding patterns (foldLeft/foldRight)
- Lazy evaluation strategies (lazy delegate)
- Sequences vs Collections
- Infinite data structures

**Sources**:
- Joy of Kotlin: Ch 8 (Memoization), Ch 9 (Laziness, Streams)
- Kotlin in Action: Ch 5 (Sequences)

**Key Patterns**:
- Stack-safe recursion
- Deferred computation

**Tone**: Theory-heavy

---

### CHƯƠNG 9: GENERICS & VARIANCE
**Mục đích**: Generic programming

**Nội dung**:
- Type parameters
- Declaration-site variance (in/out)
- Covariance & Contravariance
- Reified type parameters
- So sánh với Java wildcards (? extends, ? super)

**Sources**:
- Kotlin in Action: Ch 11 (Generics)
- Joy of Kotlin: "Using the right types"

**Key Innovation**:
- Declaration-site variance (simpler than Java)
- Reified generics

**Tone**: Balanced

## PHẦN III: ADVANCED & PRACTICAL (Chapters 10-12)

### CHƯƠNG 10: EXTENSION FUNCTIONS & DSLs
**Mục đích**: Advanced language mechanisms

**Nội dung**:
- Extension functions mechanism (Open/Closed principle)
- Lambdas with receivers
- Type-safe builders
- Internal DSLs construction (HTML builders, SQL DSLs)

**Sources**:
- Kotlin in Action: Ch 13 (Building DSLs)
- Joy of Kotlin: "Pushing abstraction further"

**Key Innovation**:
- Extension functions (không cần inheritance)
- DSL capabilities

**Tone**: Practice-heavy

---

### CHƯƠNG 11: COROUTINES
**Mục đích**: Modern concurrency

**Nội dung**:
- Problems với threads (blocking, complexity)
- Suspend functions & Continuations
- Structured concurrency
- Flow - reactive streams
- Comparison với async/await, Actors

**Sources**:
- Kotlin in Action: Ch 14-18 (Coroutines & Flows)
- Joy of Kotlin: Ch 13 (Actors - comparison)

**Key Innovation**:
- Lightweight concurrency
- Structured concurrency
- Cold flows

**Tone**: Practice-heavy

---

### CHƯƠNG 12: JAVA INTEROPERABILITY
**Mục đích**: Real-world integration

**Nội dung**:
- Platform types
- Calling Java from Kotlin (nullability annotations)
- Calling Kotlin from Java (@JvmName, @JvmStatic, etc.)
- Mixed codebases strategies
- Migration best practices

**Sources**:
- Kotlin in Action: Throughout (Java interop examples)
- Joy of Kotlin: Pragmatic approach discussion

**Key Differentiator**:
- 100% Java interoperability
- Incremental adoption

**Tone**: Practice-heavy

## Design Patterns Throughout

### Comparative Analysis Pattern
Mỗi chapter sẽ so sánh:
- **Practical approach** (Kotlin in Action)
- **Functional approach** (Joy of Kotlin)
- **Trade-offs** và design decisions

### Academic Structure Pattern
Mỗi chapter tuân theo:
1. Introduction (context)
2. Theoretical foundation
3. Concrete examples
4. Analysis và evaluation
5. Summary

## Integration Points
- Ch 3 (Types) → Ch 5 (FP) → Ch 6 (Control Flow)
- Ch 5 (FP) → Ch 8 (Laziness)
- Ch 7 (Coroutines) ← Ch 13 Joy (Actors comparison)
- Ch 9 ties everything together (pragmatism)
