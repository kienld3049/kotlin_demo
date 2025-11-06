# Kotlin Interpreter - Streamlit Web GUI

## 🌐 Overview

**Purpose**: Tạo web-based interactive GUI để visualize từng bước compilation/interpretation của Kotlin code, thay vì chỉ terminal-based output.

**Tech Stack**: Streamlit (Python web framework)

**Timeline**: ~4 giờ implementation

## 🎯 Objectives

### Educational Goals
- ✅ Hiển thị rõ ràng từng phase: Lexing → Parsing → Semantic → Execution
- ✅ Interactive exploration của AST, tokens, symbol tables
- ✅ Step-by-step execution với variable tracking
- ✅ Visual feedback tốt hơn terminal output

### User Experience Goals
- ✅ Code editor với syntax highlighting
- ✅ Real-time visualization
- ✅ Click-to-inspect functionality
- ✅ Professional, polished interface

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Web App                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌─────────────────────────┐ │
│  │              │         │  Visualization Tabs     │ │
│  │ Code Editor  │         │  ┌──────┬──────┬─────┐ │ │
│  │              │         │  │Tokens│ AST  │ ... │ │ │
│  │ • Syntax     │         │  └──────┴──────┴─────┘ │ │
│  │   highlight  │         │                         │ │
│  │ • Examples   │         │  • Tokens Table         │ │
│  │ • Controls   │         │  • AST Tree Viz         │ │
│  │              │         │  • Symbol Tables        │ │
│  └──────────────┘         │  • Execution Stepper    │ │
│                           │  • Output Console       │ │
│                           └─────────────────────────┘ │
│                                                         │
│  Phase Progress: [A]→[B]→[C]→[D]→[E]→[F]              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │ Existing Interpreter    │
              │ • Lexer                 │
              │ • Parser                │
              │ • Semantic Analyzer     │
              │ • Runtime Evaluator     │
              └─────────────────────────┘
```

## 📁 File Structure

```
kotlin_interpreter/
├── streamlit_app.py              # ⭐ Main Streamlit application
├── src/
│   ├── gui/                      # ⭐ NEW: GUI-specific code
│   │   ├── __init__.py
│   │   ├── components.py         # Reusable UI components
│   │   ├── visualizers.py        # AST tree, charts visualizations
│   │   ├── state_manager.py      # Session state management
│   │   └── examples.py           # Pre-loaded example programs
│   ├── lexer/                    # Existing
│   ├── parser/                   # Existing
│   ├── semantic/                 # Existing
│   └── runtime/                  # Existing
├── requirements.txt              # Updated with Streamlit deps
└── README.md                     # Updated with GUI instructions
```

## 🎨 UI Design

### Layout: Two-Column Design

```
┌─────────────────────────────────────────────────────────────┐
│  🚀 Kotlin Interpreter - Interactive Demo                   │
│  Mô phỏng quá trình biên dịch & thực thi Kotlin từ A→Z      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐  ┌────────────────────────────┐   │
│  │  📝 Kotlin Code     │  │  🔍 Visualization          │   │
│  ├─────────────────────┤  ├────────────────────────────┤   │
│  │                     │  │ Tabs:                      │   │
│  │ fun main() {        │  │ [🔤Tokens][🌳AST][📊Sym]  │   │
│  │   val x = 5         │  │ [⚙️Exec][📄Output]         │   │
│  │   val y = 10        │  │                            │   │
│  │   println(x + y)    │  │ ┌────────────────────────┐ │   │
│  │ }                   │  │ │                        │ │   │
│  │                     │  │ │  Content for active    │ │   │
│  ├─────────────────────┤  │ │  tab displayed here    │ │   │
│  │ Examples: ▼         │  │ │                        │ │   │
│  │ [Hello World]       │  │ │                        │ │   │
│  ├─────────────────────┤  │ └────────────────────────┘ │   │
│  │ [▶Run][⏭Step][🔄]  │  │                            │   │
│  └─────────────────────┘  └────────────────────────────┘   │
│                                                              │
│  Progress: [A]✓→[B]✓→[C]✓→[D]→→[E]→[F]                     │
└─────────────────────────────────────────────────────────────┘
```

### Tab Contents

#### 1. **🔤 Tokens Tab**
```
┌──────────────────────────────────────────────────┐
│  Token Analysis (15 tokens)                      │
├──────┬───────────┬──────────┬──────────┬─────────┤
│  #   │   Type    │  Value   │ Location │ Details │
├──────┼───────────┼──────────┼──────────┼─────────┤
│  0   │ FUN       │ fun      │ 1:1      │   🔍   │
│  1   │ IDENTIFIER│ main     │ 1:5      │   🔍   │
│  2   │ LPAREN    │ (        │ 1:9      │   🔍   │
│  3   │ RPAREN    │ )        │ 1:10     │   🔍   │
│  ... │ ...       │ ...      │ ...      │   ...   │
└──────┴───────────┴──────────┴──────────┴─────────┘

Color coding:
• Keywords (fun, val) → Blue
• Identifiers → Green
• Operators → Orange
• Literals → Yellow
```

#### 2. **🌳 AST Tree Tab**
```
Interactive Tree Visualization:
• Plotly/Graphviz interactive diagram
• Click node → Show details panel
• Collapsible subtrees
• Zoom & pan controls
• Export as PNG

         Program
            │
      FunctionDecl (main)
            │
      BlockStatement
         ┌──┼──┐
      ValDecl ValDecl ExprStmt
       (x=5)  (y=10)  (println)
```

#### 3. **📊 Symbol Tables Tab**
```
┌──────────────────────────────────────────┐
│  Scope Hierarchy                         │
├──────────────────────────────────────────┤
│  Global Scope                            │
│  └─ Functions:                           │
│     └─ main: () -> Unit                  │
│                                          │
│  Function Scope: main                    │
│  ┌────────┬──────┬─────────┬──────────┐ │
│  │ Name   │ Type │ Mutable │ Value    │ │
│  ├────────┼──────┼─────────┼──────────┤ │
│  │ x      │ Int  │ No      │ 5        │ │
│  │ y      │ Int  │ No      │ 10       │ │
│  └────────┴──────┴─────────┴──────────┘ │
└──────────────────────────────────────────┘
```

#### 4. **⚙️ Execution Tab**
```
┌──────────────────────────────────────────┐
│  Step-by-Step Execution                  │
├──────────────────────────────────────────┤
│  Current Line: 3                         │
│  > val y = 10                            │
│                                          │
│  Variable States:                        │
│  ┌────┬───────┬────────┐                │
│  │ x  │ Int   │ 5      │                │
│  │ y  │ Int   │ 10     │ ← Just set    │
│  └────┴───────┴────────┘                │
│                                          │
│  Call Stack:                             │
│  └─ main()                               │
│                                          │
│  [⏮Previous] [⏭Next] [⏸Pause]          │
└──────────────────────────────────────────┘
```

#### 5. **📄 Output Tab**
```
┌──────────────────────────────────────────┐
│  Program Output                          │
├──────────────────────────────────────────┤
│  15                                      │
│                                          │
│  ─────────────────────────────────────   │
│  ✅ Execution completed successfully     │
│                                          │
│  Statistics:                             │
│  • Time: 0.003s                          │
│  • Tokens: 15                            │
│  • AST Nodes: 8                          │
│  • Variables: 2                          │
└──────────────────────────────────────────┘
```

## 🛠️ Implementation Plan

### Phase 1: Basic Setup (30 minutes)

**Goals**: Get Streamlit running với basic layout

**Tasks**:
- [ ] Install dependencies: `streamlit`, `plotly`, `pandas`
- [ ] Create `streamlit_app.py` với basic layout
- [ ] Setup 2-column design
- [ ] Add code editor (text_area with syntax highlighting)
- [ ] Test: `streamlit run streamlit_app.py`

**Code Structure**:
```python
import streamlit as st

st.set_page_config(layout="wide", page_title="Kotlin Interpreter")

# Header
st.title("🚀 Kotlin Interpreter - Interactive Demo")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Kotlin Code")
    code = st.text_area("", height=300, value=default_code)
    
    if st.button("▶ Run"):
        # TODO: Process code
        pass

with col2:
    st.subheader("🔍 Visualization")
    tabs = st.tabs(["Tokens", "AST", "Symbols", "Exec", "Output"])
    # TODO: Tab contents
```

### Phase 2: Integration (1 hour)

**Goals**: Connect existing interpreter code

**Tasks**:
- [ ] Create `src/gui/state_manager.py` for session state
- [ ] Import existing Lexer, Parser, Semantic, Runtime
- [ ] Implement "Run" button logic:
  - Execute all phases
  - Store results in session state
  - Display in tabs
- [ ] Handle errors gracefully
- [ ] Test với hello_world.kt

**Key Code**:
```python
# state_manager.py
class InterpreterState:
    def __init__(self):
        self.tokens = None
        self.ast = None
        self.symbol_tables = None
        self.execution_steps = []
        self.output = ""
        self.errors = []
    
    def run_code(self, source_code: str):
        try:
            # Phase 1: Lexing
            lexer = Lexer(source_code)
            self.tokens = lexer.tokenize()
            
            # Phase 2: Parsing
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            # Phase 3: Semantic Analysis
            # ...
            
            # Phase 4: Execution
            # ...
            
        except Exception as e:
            self.errors.append(str(e))
```

### Phase 3: Visualizations (2 hours)

**Goals**: Implement all visualization tabs

**Tasks**:
- [ ] **Tokens Tab**: Create DataFrame từ tokens, display với st.dataframe
- [ ] **AST Tab**: Implement tree visualization với Plotly/Graphviz
- [ ] **Symbol Tables Tab**: Display scope hierarchy & variables
- [ ] **Execution Tab**: Implement step-by-step với prev/next buttons
- [ ] **Output Tab**: Display output & statistics

**Tokens Visualization**:
```python
# visualizers.py
def display_tokens(tokens):
    df = pd.DataFrame([
        {
            "Index": i,
            "Type": token.type.name,
            "Value": token.value,
            "Location": f"{token.location.line}:{token.location.column}"
        }
        for i, token in enumerate(tokens)
    ])
    
    st.dataframe(df, use_container_width=True)
```

**AST Visualization**:
```python
def display_ast_tree(ast):
    # Option 1: Plotly Tree
    fig = create_plotly_tree(ast)
    st.plotly_chart(fig, use_container_width=True)
    
    # Option 2: Graphviz
    graph = create_graphviz_tree(ast)
    st.graphviz_chart(graph)
```

### Phase 4: Polish (30 minutes)

**Goals**: Enhance UX and add finishing touches

**Tasks**:
- [ ] Add example programs dropdown
- [ ] Implement step controls (prev/next)
- [ ] Add progress indicator visualization
- [ ] Improve error display với colors
- [ ] Add tooltips and help text
- [ ] Make responsive for different screen sizes
- [ ] Add dark mode support (optional)

**Example Selector**:
```python
# examples.py
EXAMPLES = {
    "Hello World": """
fun main() {
    println("Hello World")
}
""",
    "Variables": """
fun main() {
    val x = 5
    val y = 10
    println(x + y)
}
""",
    "Functions": """
fun add(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val result = add(5, 10)
    println(result)
}
"""
}
```

## 📦 Dependencies

### New Requirements
```txt
# Add to requirements.txt

# Streamlit Framework
streamlit>=1.28.0
streamlit-ace>=0.1.1        # Code editor with syntax highlighting

# Visualization
plotly>=5.17.0              # Interactive charts
pandas>=2.0.0               # Data manipulation
graphviz>=0.20.0            # Graph visualization

# Optional enhancements
streamlit-extras>=0.3.0     # Extra components
streamlit-agraph>=0.0.45    # Graph visualization alternative
```

### Installation
```bash
cd kotlin_interpreter
pip install -r requirements.txt
```

## 🚀 Running the App

### Development Mode
```bash
cd kotlin_interpreter
streamlit run streamlit_app.py
```

Opens browser at `http://localhost:8501`

### Production Deployment Options

**1. Streamlit Cloud** (Easiest)
- Push to GitHub
- Connect Streamlit Cloud
- Auto-deploy

**2. Docker**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

**3. VPS/Server**
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🎓 Educational Features

### Interactive Learning
- **Hover tooltips**: Explain technical terms
- **Click-to-inspect**: Deep dive into any node/token
- **Step-by-step mode**: Understand execution flow
- **Example programs**: Learn from working code

### Visual Feedback
- **Color coding**: Different colors for different token/node types
- **Progress tracking**: See which phase is active
- **Error highlighting**: Point to exact problem location
- **Statistics**: Understand performance characteristics

## 🔄 Comparison with Terminal Modes

| Feature | Terminal (Verbose) | Streamlit GUI |
|---------|-------------------|---------------|
| **Accessibility** | CLI only | Web browser |
| **Interactivity** | Linear output | Click-to-explore |
| **Visualization** | Text-based | Graphics + Charts |
| **Step Control** | No | Yes (prev/next) |
| **Code Editing** | External editor | Built-in editor |
| **Sharing** | Copy/paste | Share URL |
| **Learning Curve** | Steeper | Gentler |

**When to use Terminal**:
- ✅ Automation/scripting
- ✅ CI/CD pipelines
- ✅ Quick tests
- ✅ No GUI available

**When to use Streamlit GUI**:
- ✅ Education/teaching
- ✅ Demos/presentations
- ✅ Interactive exploration
- ✅ Debugging complex code

## 📊 Success Metrics

### Technical Metrics
- [ ] Loading time < 2s
- [ ] Responsive on mobile/tablet
- [ ] No crashes on invalid input
- [ ] Support Kotlin files up to 500 lines

### User Experience Metrics
- [ ] Intuitive navigation (< 5 min to learn)
- [ ] Clear visualization of all phases
- [ ] Helpful error messages
- [ ] Smooth step-by-step execution

## 🎯 Future Enhancements

### Phase 2 (Post-MVP)
- [ ] **Dark mode toggle**: User preference
- [ ] **Export results**: Download AST, tokens as JSON/PNG
- [ ] **Code snippets library**: More examples
- [ ] **Collaborative editing**: Share session with others
- [ ] **Performance profiling**: Show execution time per operation

### Phase 3 (Advanced)
- [ ] **Multi-file support**: Import/export modules
- [ ] **Breakpoints**: Set execution breakpoints
- [ ] **Variable watch**: Track specific variables
- [ ] **Comparison mode**: Compare two programs side-by-side
- [ ] **AI assistance**: Explain code with GPT integration

## ✅ Implementation Checklist

### Setup
- [ ] Install Streamlit dependencies
- [ ] Create streamlit_app.py
- [ ] Setup project structure (src/gui/)

### Core Features
- [ ] Code editor panel
- [ ] Tokens visualization
- [ ] AST tree visualization
- [ ] Symbol tables display
- [ ] Execution stepper
- [ ] Output console

### Polish
- [ ] Example programs
- [ ] Error handling
- [ ] Progress indicator
- [ ] Responsive design
- [ ] Documentation

### Testing
- [ ] Test with hello_world.kt
- [ ] Test with complex programs
- [ ] Test error scenarios
- [ ] Cross-browser testing

## 📝 Notes

- Streamlit auto-reloads on file changes (great for development)
- Session state persists during reruns
- Can deploy for free on Streamlit Cloud
- Perfect for educational/demo purposes
- Python-only (no JavaScript needed)
