"""
Kotlin Interpreter - Streamlit Web GUI
Demo mô phỏng cách hoạt động của ngôn ngữ Kotlin từ A đến Z
"""

import streamlit as st
import pandas as pd
from src.gui.state_manager import StateManager
from src.semantic.symbol_table import SymbolKind
import json
import graphviz

# Page config
st.set_page_config(
    page_title="Kotlin Interpreter Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #7F52FF;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .step-header {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
StateManager.initialize()
state = StateManager.get_state()

# Header
st.markdown('<div class="main-header">🚀 Kotlin Interpreter Demo</div>', unsafe_allow_html=True)
st.markdown("### Mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z")

# Sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình")
    
    # Example programs
    st.subheader("📚 Chương trình mẫu")
    examples = StateManager.get_example_programs()
    selected_example = st.selectbox(
        "Chọn ví dụ:",
        ["-- Custom Code --"] + list(examples.keys())
    )
    
    if selected_example != "-- Custom Code --":
        if st.button("📥 Load Example"):
            StateManager.update_source_code(examples[selected_example])
            st.rerun()
    
    st.divider()
    
    # Settings
    st.subheader("🔧 Tùy chọn")
    show_tokens = st.checkbox("Hiển thị Tokens", value=True)
    show_ast = st.checkbox("Hiển thị AST", value=True)
    show_symbols = st.checkbox("Hiển thị Symbol Table", value=True)
    show_output = st.checkbox("Hiển thị Output", value=True)
    
    st.divider()
    
    # Clear button
    if st.button("🗑️ Clear All", use_container_width=True):
        StateManager.clear_state()
        st.rerun()
    
    st.divider()
    
    # Info
    st.info("""
    **Các bước xử lý:**
    1. 📝 Lexical Analysis
    2. 🌳 Syntax Analysis (Parsing)
    3. 🔍 Semantic Analysis
    4. ⚡ Execution
    """)

# Main content - 2 columns
col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("📝 Source Code")
    
    # Code editor
    source_code = st.text_area(
        "Nhập code Kotlin:",
        value=state.source_code,
        height=400,
        placeholder='''fun main() {
    println("Hello, World!")
}''',
        key="code_editor"
    )
    
    # Buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        run_button = st.button("▶️ Run", type="primary", use_container_width=True)
    with btn_col2:
        clear_code = st.button("🧹 Clear Code", use_container_width=True)
    
    if clear_code:
        StateManager.update_source_code("")
        st.rerun()
    
    # Run interpreter
    if run_button and source_code.strip():
        with st.spinner("🔄 Đang xử lý..."):
            result = StateManager.run_interpreter(source_code)
        
        if result['success']:
            st.success("✅ Thực thi thành công!")
        else:
            st.error("❌ Có lỗi xảy ra!")

with col_right:
    st.header("📊 Kết quả phân tích")
    
    # Tabs for different views
    tabs = st.tabs(["🖥️ Output", "🔤 Tokens", "🌳 AST", "📋 Symbols"])
    
    # Tab 1: Output
    with tabs[0]:
        if show_output and state.output:
            st.subheader("Output của chương trình:")
            st.code(state.output, language="text")
        elif state.errors:
            st.error("**Errors:**")
            for error in state.errors:
                st.code(error, language="text")
        else:
            st.info("Nhấn 'Run' để xem kết quả")
    
    # Tab 2: Tokens
    with tabs[1]:
        if show_tokens and state.tokens:
            st.subheader("Lexical Analysis - Tokens")
            
            # Convert tokens to DataFrame
            token_data = []
            for i, token in enumerate(state.tokens):
                token_data.append({
                    "Index": i,
                    "Type": token.type.value,
                    "Value": str(token.value),
                    "Line": token.location.line,
                    "Column": token.location.column
                })
            
            df = pd.DataFrame(token_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Statistics
            st.metric("Tổng số tokens", len(state.tokens))
            
        elif state.tokens:
            st.info("Bật 'Hiển thị Tokens' trong sidebar để xem")
        else:
            st.info("Chưa có tokens. Nhấn 'Run' để phân tích.")
    
    # Tab 3: AST
    with tabs[2]:
        if show_ast and state.ast:
            st.subheader("Syntax Analysis - Abstract Syntax Tree")
            
            # View toggle
            view_mode = st.radio(
                "Chọn chế độ xem:",
                ["📊 Graph View", "📄 JSON View"],
                horizontal=True
            )
            
            if view_mode == "📊 Graph View":
                # Graph visualization
                def ast_to_graphviz(node, graph=None, parent_id=None, counter=[0], edge_label=""):
                    """Convert AST to Graphviz diagram with enhanced visualization"""
                    if node is None:
                        return graph
                    
                    if graph is None:
                        graph = graphviz.Digraph()
                        graph.attr(rankdir='TB')  # Top to Bottom
                        graph.attr('node', shape='box', style='filled')
                        graph.attr('edge', fontsize='10', fontcolor='gray')
                    
                    # Generate unique ID
                    node_id = f"node_{counter[0]}"
                    counter[0] += 1
                    
                    # Create label with class name
                    node_type = node.__class__.__name__
                    label = node_type
                    
                    # Determine color based on node type
                    color = 'lightblue'  # default
                    if 'Function' in node_type:
                        color = 'lightgreen'
                    elif 'Variable' in node_type or 'Declaration' in node_type:
                        color = 'lightyellow'
                    elif 'Expression' in node_type:
                        color = 'lightcoral'
                    elif 'Literal' in node_type:
                        color = 'orange'
                    elif 'Statement' in node_type:
                        color = 'lightcyan'
                    
                    # Add key attributes to label
                    # Check function_name FIRST (for CallExpression)
                    if hasattr(node, 'function_name') and node.function_name:
                        label += f"\\nfunc: {node.function_name}"
                    elif hasattr(node, 'name') and node.name:
                        # For other nodes like FunctionDeclaration, VariableDeclaration, IdentifierExpression
                        label += f"\\nname: {node.name}"
                    
                    if hasattr(node, 'value') and node.value is not None:
                        val_str = str(node.value)
                        if len(val_str) > 20:
                            val_str = val_str[:20] + "..."
                        label += f"\\nvalue: {val_str}"
                    
                    if hasattr(node, 'operator') and node.operator:
                        label += f"\\nop: {node.operator}"
                    
                    if hasattr(node, 'literal_type') and node.literal_type:
                        label += f"\\ntype: {node.literal_type}"
                    
                    if hasattr(node, 'is_mutable'):
                        label += f"\\n{'var' if node.is_mutable else 'val'}"
                    
                    if hasattr(node, 'return_type') and node.return_type:
                        label += f"\\nreturns: {node.return_type}"
                    
                    # Add node to graph with color
                    graph.node(node_id, label, fillcolor=color)
                    
                    # Connect to parent with labeled edge
                    if parent_id:
                        graph.edge(parent_id, node_id, label=edge_label)
                    
                    # Recursively process children with labeled edges
                    for attr in dir(node):
                        if attr.startswith('_') or attr in ['accept', 'visit', 'location']:
                            continue
                        
                        try:
                            value = getattr(node, attr)
                            if callable(value) or value is None:
                                continue
                            
                            # Skip primitive attributes already in label
                            if attr in ['name', 'value', 'operator', 'literal_type', 'function_name', 
                                       'is_mutable', 'return_type', 'type']:
                                continue
                            
                            if isinstance(value, list):
                                for i, item in enumerate(value):
                                    if hasattr(item, '__class__') and hasattr(item, '__dict__'):
                                        # Create edge label with attribute name and index
                                        label = f"{attr}[{i}]" if len(value) > 1 else attr
                                        ast_to_graphviz(item, graph, node_id, counter, label)
                            elif hasattr(value, '__class__') and hasattr(value, '__dict__'):
                                # Skip SourceLocation and other non-AST objects
                                if value.__class__.__name__ not in ['SourceLocation', 'str', 'int', 'bool']:
                                    # Use attribute name as edge label
                                    ast_to_graphviz(value, graph, node_id, counter, attr)
                        except Exception:
                            continue
                    
                    return graph
                
                try:
                    graph = ast_to_graphviz(state.ast)
                    st.graphviz_chart(graph.source)
                except Exception as e:
                    st.error(f"Lỗi khi tạo graph: {str(e)}")
                    st.info("Chuyển sang JSON View để xem chi tiết")
            
            else:
                # JSON view
                def ast_to_dict(node, depth=0, max_depth=10):
                    """Convert AST node to dict for display with proper recursion"""
                    if node is None:
                        return None
                    
                    if depth > max_depth:
                        return {"type": node.__class__.__name__, "...": "max depth reached"}
                    
                    # Base case: primitive types
                    if isinstance(node, (str, int, float, bool)):
                        return node
                    
                    # Check if it's an AST node
                    if not hasattr(node, '__class__'):
                        return str(node)
                    
                    result = {"type": node.__class__.__name__}
                    
                    # Get all attributes except private and methods
                    for attr in dir(node):
                        if attr.startswith('_') or attr in ['accept', 'visit']:
                            continue
                        
                        try:
                            value = getattr(node, attr)
                            if callable(value):
                                continue
                            
                            # Handle different types of values
                            if value is None:
                                result[attr] = None
                            elif isinstance(value, (str, int, float, bool)):
                                result[attr] = value
                            elif isinstance(value, list):
                                # Recursively process list items
                                result[attr] = [
                                    ast_to_dict(item, depth + 1, max_depth) 
                                    if hasattr(item, '__class__') and not isinstance(item, (str, int, float, bool))
                                    else item
                                    for item in value
                                ]
                            elif hasattr(value, '__dict__'):
                                # It's an object, recurse into it
                                result[attr] = ast_to_dict(value, depth + 1, max_depth)
                            else:
                                result[attr] = str(value)
                        except Exception:
                            # Skip attributes that cause errors
                            continue
                    
                    return result
                
                ast_dict = ast_to_dict(state.ast)
                st.json(ast_dict, expanded=1)
            
        elif state.ast:
            st.info("Bật 'Hiển thị AST' trong sidebar để xem")
        else:
            st.info("Chưa có AST. Nhấn 'Run' để phân tích.")
    
    # Tab 4: Symbol Table
    with tabs[3]:
        if show_symbols and state.symbol_table:
            st.subheader("Semantic Analysis - Symbol Table")
            
            # Get all symbols from global scope
            symbols = state.symbol_table.global_scope.symbols
            
            # Separate functions and variables
            functions = {name: sym for name, sym in symbols.items() 
                        if sym.kind == SymbolKind.FUNCTION}
            variables = {name: sym for name, sym in symbols.items() 
                        if sym.kind == SymbolKind.VARIABLE}
            
            # Display Functions
            if functions:
                st.write("**Functions:**")
                func_data = []
                for name, func_sym in functions.items():
                    # func_sym is FunctionSymbol
                    params = ", ".join(func_sym.parameter_types)
                    func_data.append({
                        "Name": name,
                        "Parameters": f"({params})",
                        "Return Type": func_sym.return_type
                    })
                if func_data:
                    st.dataframe(pd.DataFrame(func_data), 
                               use_container_width=True, hide_index=True)
            
            # Display Variables
            if variables:
                st.write("**Variables (Global Scope):**")
                var_data = []
                for name, var_sym in variables.items():
                    var_data.append({
                        "Name": name,
                        "Type": var_sym.type,
                        "Mutable": "var" if var_sym.is_mutable else "val"
                    })
                if var_data:
                    st.dataframe(pd.DataFrame(var_data), 
                               use_container_width=True, hide_index=True)
            
        elif state.symbol_table:
            st.info("Bật 'Hiển thị Symbol Table' trong sidebar để xem")
        else:
            st.info("Chưa có Symbol Table. Nhấn 'Run' để phân tích.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 Kotlin Interpreter Demo - Bài tập lớn Nguyên lý Ngôn ngữ lập trình</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Display errors if any
if state.errors:
    st.divider()
    with st.expander("⚠️ Chi tiết lỗi", expanded=True):
        for i, error in enumerate(state.errors, 1):
            st.error(f"**Error {i}:** {error}")
