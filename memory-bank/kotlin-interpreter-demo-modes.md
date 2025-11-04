# Kotlin Interpreter - Demo Modes & User Experience

## 🎬 User Experience Design

### Core Philosophy
Demo phải:
- ✅ **Educational**: Hiển thị rõ từng bước compilation/interpretation
- ✅ **Interactive**: Cho phép explore và inspect
- ✅ **Visual**: Dễ hiểu qua visualizations
- ✅ **Professional**: Output đẹp, polished

## 🎭 Demo Modes

### 1. Verbose Mode (`--verbose`)

**Purpose**: Hiển thị chi tiết từng bước cho educational purposes

**Usage**:
```bash
python main.py examples/hello_world.kt --verbose
```

**Output Example**:
```
╔════════════════════════════════════════════════════════════╗
║         KOTLIN INTERPRETER - VERBOSE MODE                  ║
╚════════════════════════════════════════════════════════════╝

📄 Source Code: examples/hello_world.kt
────────────────────────────────────────────────────────────
1 | fun main() {
2 |     val x = 5
3 |     val y = 10
4 |     println(x + y)
5 | }
────────────────────────────────────────────────────────────

[PHASE 1] 🔤 LEXICAL ANALYSIS
────────────────────────────────────────────────────────────
┏━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ # ┃ Type       ┃ Value   ┃ Location ┃
┡━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ 0   │ FUN        │ fun     │ 1:1      │
│ 1   │ IDENTIFIER │ main    │ 1:5      │
│ 2   │ LPAREN     │ (       │ 1:9      │
│ 3   │ RPAREN     │ )       │ 1:10     │
│ 4   │ LBRACE     │ {       │ 1:12     │
│ 5   │ VAL        │ val     │ 2:5      │
│ 6   │ IDENTIFIER │ x       │ 2:9      │
│ 7   │ ASSIGN     │ =       │ 2:11     │
│ 8   │ INT_LITERAL│ 5       │ 2:13     │
│ ... │ ...        │ ...     │ ...      │
└─────┴────────────┴─────────┴──────────┘

✅ Lexer completed: 15 tokens generated
────────────────────────────────────────────────────────────

[PHASE 2] 🌳 SYNTAX ANALYSIS
────────────────────────────────────────────────────────────
Building Abstract Syntax Tree...

Function Declaration: main
├─ Parameters: []
├─ Return Type: Unit (inferred)
└─ Body: Block
    ├─ Statement 1: ValDecl
    │   ├─ Name: x
    │   └─ Initializer: Literal(5, Int)
    ├─ Statement 2: ValDecl
    │   ├─ Name: y
    │   └─ Initializer: Literal(10, Int)
    └─ Statement 3: ExpressionStatement
        └─ FunctionCall(println)
            └─ Argument: BinaryExpr(+)
                ├─ Left: Identifier(x)
                └─ Right: Identifier(y)

✅ Parser completed: AST with 8 nodes
────────────────────────────────────────────────────────────

[PHASE 3] 🔍 SEMANTIC ANALYSIS
────────────────────────────────────────────────────────────

Pass 1: Declaration Collection
  ✓ Collected function: main() -> Unit

Pass 2: Type Checking
  Entering function: main
  
  [Step 1] val x = 5
    ├─ Analyzing initializer: Literal(5)
    │  └─ Type: Int
    ├─ Type inference: x: Int
    └─ ✓ Added to symbol table
  
  [Step 2] val y = 10
    ├─ Analyzing initializer: Literal(10)
    │  └─ Type: Int
    ├─ Type inference: y: Int
    └─ ✓ Added to symbol table
  
  [Step 3] println(x + y)
    ├─ Resolving 'x': Found Int
    ├─ Resolving 'y': Found Int
    ├─ Checking operator '+': Int + Int -> Int ✓
    └─ Function call: println(Int) ✓

Symbol Table (Scope: main):
┏━━━━━━━┳━━━━━━┳━━━━━━━━━┓
┃ Name  ┃ Type ┃ Mutable ┃
┡━━━━━━━╇━━━━━━╇━━━━━━━━━┩
│ x     │ Int  │ No      │
│ y     │ Int  │ No      │
└───────┴──────┴─────────┘

✅ Semantic analysis completed: No errors
────────────────────────────────────────────────────────────

[PHASE 4] 🚀 EXECUTION
────────────────────────────────────────────────────────────

Executing: main()

  [Step 1] val x = 5
    └─ ✓ x = KotlinInt(5)
    
  [Step 2] val y = 10
    └─ ✓ y = KotlinInt(10)
    
  [Step 3] println(x + y)
    ├─ Evaluating: x + y
    │  ├─ x = KotlinInt(5)
    │  ├─ y = KotlinInt(10)
    │  └─ Result = KotlinInt(15)
    └─ Calling: println(KotlinInt(15))

╔════════════════════════════════════════════════════════════╗
║                    PROGRAM OUTPUT                          ║
╠════════════════════════════════════════════════════════════╣
║  15                                                        ║
╚════════════════════════════════════════════════════════════╝

✅ Execution completed (0.003s)
```

### 2. Quiet Mode (default)

**Purpose**: Chỉ hiển thị output cuối cùng hoặc errors

**Usage**:
```bash
python main.py examples/hello_world.kt
```

**Output Example** (success):
```
15
```

**Output Example** (error):
```
❌ Error in examples/type_error.kt:2:9
Type mismatch: expected Int, got String

  1 | fun main() {
> 2 |     val x: Int = "hello"
                  ~~~~~~~~~~~
  3 | }

1 error found. Compilation failed.
```

### 3. Interactive Mode (`--interactive`)

**Purpose**: Step-through execution với inspection

**Usage**:
```bash
python main.py examples/hello_world.kt --interactive
```

**Interactive Commands**:
- `next` / `n`: Execute next step
- `continue` / `c`: Run to completion
- `inspect <var>`: Show variable value
- `scope`: Show current scope's symbol table
- `ast`: Show current AST node
- `quit` / `q`: Exit

**Session Example**:
```
🎮 Interactive Mode - Type 'help' for commands
────────────────────────────────────────────────

[Paused at] Phase 1: Lexical Analysis
> next

✓ Lexing completed: 15 tokens

[Paused at] Phase 2: Syntax Analysis
> next

✓ Parsing completed: AST with 8 nodes

[Paused at] Phase 3: Semantic Analysis (Pass 1)
> next

✓ Collection completed

[Paused at] Phase 3: Semantic Analysis (Pass 2)
> next

✓ Type checking completed

[Paused at] Phase 4: Execution - Statement 1
Current statement: val x = 5
> next

✓ Executed: x = 5

[Paused at] Phase 4: Execution - Statement 2
Current statement: val y = 10
> inspect x

Variable: x
├─ Value: 5
├─ Type: Int
└─ Mutable: No

> scope

Current Scope: main
┏━━━━━━━┳━━━━━━┳━━━━━━━━━┓
┃ Name  ┃ Type ┃ Mutable ┃
┡━━━━━━━╇━━━━━━╇━━━━━━━━━┩
│ x     │ Int  │ No      │
└───────┴──────┴─────────┘

> continue

✓ Executed: y = 10
✓ Executed: println(x + y)

Program Output: 15

✅ Execution completed
```

### 4. Visualize Mode (`--visualize`)

**Purpose**: Tạo visual representations của AST và execution

**Usage**:
```bash
python main.py examples/hello_world.kt --visualize
```

**Generated Files**:
- `ast_output.png`: AST tree diagram
- `scope_hierarchy.png`: Scope structure
- `execution_trace.html`: Interactive execution timeline

**Console Output**:
```
[PHASE 2] Syntax Analysis
✓ AST generated
📊 Visualization saved to: ast_output.png

[PHASE 3] Semantic Analysis
✓ Type checking completed
📊 Scope hierarchy saved to: scope_hierarchy.png

[PHASE 4] Execution
✓ Program executed successfully
📊 Execution trace saved to: execution_trace.html

Output: 15

💡 Open visualizations:
   - AST: ast_output.png
   - Scopes: scope_hierarchy.png
   - Timeline: execution_trace.html
```

## 🎨 Visualization Details

### AST Visualization (Graphviz)

```
          ┌─────────────┐
          │   Program   │
          └──────┬──────┘
                 │
          ┌──────▼──────────┐
          │  FunctionDecl   │
          │  name: main     │
          │  type: ()->Unit │
          └──────┬──────────┘
                 │
          ┌──────▼────────┐
          │ BlockStatement│
          └──────┬────────┘
           ┌─────┼─────┐
           │     │     │
        ┌──▼─┐ ┌─▼─┐ ┌─▼──────┐
        │Val │ │Val│ │ExprStmt│
        │x:Int│ │y:Int│─────┬──┘
        │ =5  │ │=10│      │
        └────┘ └───┘   ┌───▼────────┐
                        │ FuncCall   │
                        │  println   │
                        └───┬────────┘
                            │
                      ┌─────▼──────┐
                      │ BinaryExpr │
                      │    PLUS    │
                      └─┬────────┬─┘
                        │        │
                   ┌────▼──┐  ┌──▼────┐
                   │ Id(x) │  │ Id(y) │
                   └───────┘  └───────┘
```

### Scope Hierarchy Visualization

```
Global Scope
│
├─ Functions:
│  └─ main: () -> Unit
│
└─ Scopes:
   └─ main (function scope)
      ├─ x: Int (immutable)
      └─ y: Int (immutable)
```

### Execution Trace (HTML Timeline)

Interactive HTML với:
- Timeline của execution
- Variable states at each step
- Click để xem details
- Highlight active code lines

## 🎯 Output Formatting Standards

### Color Scheme (Rich library)
- **Cyan**: Phase headers, titles
- **Green**: Success messages, types
- **Yellow**: Warnings, values
- **Red**: Errors
- **Blue**: Locations, metadata
- **Magenta**: Keywords

### Icons
- 🔤 Lexical Analysis
- 🌳 Syntax Analysis
- 🔍 Semantic Analysis
- 🚀 Execution
- ✅ Success
- ❌ Error
- ⚠️ Warning
- 📊 Visualization
- 💡 Hint/Tip
- 🎮 Interactive prompt

## 🚨 Error Reporting

### Error Format
```
❌ [ErrorType] in file.kt:line:column
Description of the error

Context (3 lines before/after):
  line-2 | code
  line-1 | code
> line   | problematic code
           ^^^^^^^^^^^^^^ (highlight)
  line+1 | code
  line+2 | code

💡 Hint: Possible fix or explanation
```

### Multiple Errors
```
Found 3 errors:

❌ Type Error in main.kt:5:12
   Expected Int, got String

❌ Undefined Variable in main.kt:8:9
   Variable 'z' is not defined

❌ Type Mismatch in main.kt:10:5
   Cannot assign String to Int variable

3 errors found. Compilation failed.
```

## 📊 Statistics Display

```
────────────────────────────────────────────────
📊 COMPILATION STATISTICS
────────────────────────────────────────────────
Source file:        examples/hello_world.kt
Lines of code:      5
Total time:         0.045s

Phase breakdown:
  Lexing:           0.001s (2%)
  Parsing:          0.008s (18%)
  Semantic:         0.015s (33%)
  Execution:        0.021s (47%)

Memory usage:
  Tokens:           15
  AST nodes:        8
  Symbols:          2
  
Runtime stats:
  Functions called: 1
  Variables used:   2
  Operations:       1 (addition)
────────────────────────────────────────────────
```

## 🎓 Educational Features

### Hover Help (Interactive Mode)
```
> help inspect

COMMAND: inspect <variable>
Shows detailed information about a variable

Examples:
  inspect x          # Show variable x
  inspect main       # Show function main

Information shown:
  - Current value
  - Type
  - Mutability
  - Location defined
  - Usage count
```

### Explanation Mode (`--explain`)
```bash
python main.py examples/hello_world.kt --verbose --explain
```

**Extra explanations added**:
```
[Step] val x = 5

📖 Explanation:
   This is a variable declaration using 'val' (immutable).
   - 'val' means the value cannot be changed later
   - Type is inferred as 'Int' from the literal 5
   - The variable 'x' is now in the current scope
```

## 🎬 Demo Presentation Mode

**Special mode for presentations**:
```bash
python main.py examples/hello_world.kt --demo
```

**Features**:
- Animated transitions
- Slower execution
- Auto-pause at key steps
- Large, clear text
- Automatic screenshots
- Presentation-ready output

## ✅ Implementation Checklist

- [ ] Implement verbose mode output
- [ ] Implement quiet mode output
- [ ] Implement interactive mode
- [ ] Implement visualize mode
- [ ] Create AST visualizer with graphviz
- [ ] Create scope hierarchy visualizer
- [ ] Implement execution trace HTML generator
- [ ] Implement error formatting with context
- [ ] Implement statistics collection
- [ ] Add color scheme with rich library
- [ ] Create help system for interactive mode
- [ ] Implement explanation mode
- [ ] Create demo presentation mode
- [ ] Test all modes thoroughly
- [ ] Create documentation for each mode
