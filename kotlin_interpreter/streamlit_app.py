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
    st.header("📊 Compiler Pipeline (A → Z)")
    
    # Helper functions for AST visualization
    def ast_to_graphviz(node, graph=None, parent_id=None, counter=[0], edge_label=""):
        """Convert AST to Graphviz diagram with enhanced visualization"""
        if node is None:
            return graph
        
        if graph is None:
            graph = graphviz.Digraph()
            graph.attr(rankdir='TB')
            graph.attr('node', shape='box', style='filled')
            graph.attr('edge', fontsize='10', fontcolor='gray')
        
        node_id = f"node_{counter[0]}"
        counter[0] += 1
        
        node_type = node.__class__.__name__
        label = node_type
        
        # Determine color based on node type
        color = 'lightblue'
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
        if hasattr(node, 'function_name') and node.function_name:
            label += f"\\nfunc: {node.function_name}"
        elif hasattr(node, 'name') and node.name:
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
        
        graph.node(node_id, label, fillcolor=color)
        
        if parent_id:
            graph.edge(parent_id, node_id, label=edge_label)
        
        # Recursively process children
        for attr in dir(node):
            if attr.startswith('_') or attr in ['accept', 'visit', 'location']:
                continue
            
            try:
                value = getattr(node, attr)
                if callable(value) or value is None:
                    continue
                
                if attr in ['name', 'value', 'operator', 'literal_type', 'function_name', 
                           'is_mutable', 'return_type', 'type']:
                    continue
                
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        if hasattr(item, '__class__') and hasattr(item, '__dict__'):
                            label = f"{attr}[{i}]" if len(value) > 1 else attr
                            ast_to_graphviz(item, graph, node_id, counter, label)
                elif hasattr(value, '__class__') and hasattr(value, '__dict__'):
                    if value.__class__.__name__ not in ['SourceLocation', 'str', 'int', 'bool']:
                        ast_to_graphviz(value, graph, node_id, counter, attr)
            except Exception:
                continue
        
        return graph
    
    def ast_to_dict(node, depth=0, max_depth=10):
        """Convert AST node to dict for display"""
        if node is None:
            return None
        
        if depth > max_depth:
            return {"type": node.__class__.__name__, "...": "max depth reached"}
        
        if isinstance(node, (str, int, float, bool)):
            return node
        
        if not hasattr(node, '__class__'):
            return str(node)
        
        result = {"type": node.__class__.__name__}
        
        for attr in dir(node):
            if attr.startswith('_') or attr in ['accept', 'visit']:
                continue
            
            try:
                value = getattr(node, attr)
                if callable(value):
                    continue
                
                if value is None:
                    result[attr] = None
                elif isinstance(value, (str, int, float, bool)):
                    result[attr] = value
                elif isinstance(value, list):
                    result[attr] = [
                        ast_to_dict(item, depth + 1, max_depth) 
                        if hasattr(item, '__class__') and not isinstance(item, (str, int, float, bool))
                        else item
                        for item in value
                    ]
                elif hasattr(value, '__dict__'):
                    result[attr] = ast_to_dict(value, depth + 1, max_depth)
                else:
                    result[attr] = str(value)
            except Exception:
                continue
        
        return result
    
    # Check if anything has been processed
    if not state.output and not state.errors and not state.tokens and not state.ast:
        st.info("👈 Nhấn 'Run' ở bên trái để xem toàn bộ pipeline phân tích")
    
    # ---- STEP 1: LEXICAL ANALYSIS ----
    st.subheader("🔤 Bước 1: Lexical Analysis (Phân tích Từ vựng)")
    
    if show_tokens and state.tokens:
        with st.container():
            st.markdown("""
            <div class="info-box">
                <strong>💡 Tại sao cần bước này?</strong><br>
                Máy tính không hiểu code dạng text. Lexer chia nhỏ code thành các "từ" (tokens) có ý nghĩa.<br>
                Giống như khi đọc tiếng Việt, bạn cần tách câu thành từng từ!
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("📥 **Input:** Source Code (text)")
            st.caption("⚙️ **Process:** Tokenization - chia nhỏ thành tokens")
            st.caption(f"📤 **Output:** {len(state.tokens)} tokens")
            
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
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tổng số tokens", len(state.tokens))
            with col2:
                unique_types = len(set(token.type.value for token in state.tokens))
                st.metric("Loại tokens", unique_types)
    elif not state.tokens:
        st.info("Chưa có tokens. Nhấn 'Run' để phân tích.")
    else:
        st.info("Bật 'Hiển thị Tokens' trong sidebar để xem")
    
    # Visual separator
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <span style='font-size: 24px;'>⬇️</span><br>
            <span style='color: #666; font-size: 12px;'>tokens được chuyển đến Parser</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    # ---- STEP 2: SYNTAX ANALYSIS ----
    st.subheader("🌳 Bước 2: Syntax Analysis (Phân tích Cú pháp)")
    
    if show_ast and state.ast:
        with st.container():
            st.markdown("""
            <div class="info-box">
                <strong>💡 Tại sao cần bước này?</strong><br>
                Sau khi có "từ", cần hiểu "ngữ pháp" (cấu trúc câu).<br>
                AST (Abstract Syntax Tree) là cây biểu diễn cấu trúc logic của code.
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("📥 **Input:** Danh sách Tokens")
            st.caption("⚙️ **Process:** Parsing - xây dựng cây cú pháp")
            st.caption("📤 **Output:** Abstract Syntax Tree (AST)")
            
            # View mode selection
            view_mode = st.radio(
                "Chọn chế độ xem AST:",
                ["📊 Graph View", "📄 JSON View"],
                horizontal=True,
                key="ast_view_mode"
            )
            
            if view_mode == "📊 Graph View":
                try:
                    graph = ast_to_graphviz(state.ast)
                    st.graphviz_chart(graph.source)
                except Exception as e:
                    st.error(f"Lỗi khi tạo graph: {str(e)}")
                    st.info("Chuyển sang JSON View để xem chi tiết")
            else:
                ast_dict = ast_to_dict(state.ast)
                st.json(ast_dict, expanded=1)
                
    elif not state.ast:
        st.info("Chưa có AST. Nhấn 'Run' để phân tích.")
    else:
        st.info("Bật 'Hiển thị AST' trong sidebar để xem")
    
    # Visual separator
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <span style='font-size: 24px;'>⬇️</span><br>
            <span style='color: #666; font-size: 12px;'>AST được chuyển đến Semantic Analyzer</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    # ---- STEP 3: SEMANTIC ANALYSIS ----
    st.subheader("📋 Bước 3: Semantic Analysis (Phân tích Ngữ nghĩa)")
    
    if show_symbols and state.symbol_table:
        with st.container():
            st.markdown("""
            <div class="info-box">
                <strong>💡 Tại sao cần bước này?</strong><br>
                Kiểm tra "ngữ nghĩa" - ý nghĩa của code có đúng không?<br>
                Thu thập các khai báo (functions, variables), kiểm tra types, phát hiện lỗi.
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("📥 **Input:** Abstract Syntax Tree")
            st.caption("⚙️ **Process:** Type checking, symbol collection")
            st.caption("📤 **Output:** Symbol Table (bảng ký hiệu)")
            
            # Get all symbols from global scope
            symbols = state.symbol_table.global_scope.symbols
            
            # Separate functions and variables
            functions = {name: sym for name, sym in symbols.items() 
                        if sym.kind == SymbolKind.FUNCTION}
            variables = {name: sym for name, sym in symbols.items() 
                        if sym.kind == SymbolKind.VARIABLE}
            
            # Display in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                if functions:
                    st.write("**🔧 Functions:**")
                    func_data = []
                    for name, func_sym in functions.items():
                        params = ", ".join(func_sym.parameter_types)
                        func_data.append({
                            "Name": name,
                            "Parameters": f"({params})",
                            "Return Type": func_sym.return_type
                        })
                    if func_data:
                        st.dataframe(pd.DataFrame(func_data), 
                                   use_container_width=True, hide_index=True)
                else:
                    st.info("Không có functions")
            
            with col2:
                if variables:
                    st.write("**📦 Variables:**")
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
                else:
                    st.info("Không có variables")
                    
    elif not state.symbol_table:
        st.info("Chưa có Symbol Table. Nhấn 'Run' để phân tích.")
    else:
        st.info("Bật 'Hiển thị Symbol Table' trong sidebar để xem")
    
    # Visual separator
    st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <span style='font-size: 24px;'>⬇️</span><br>
            <span style='color: #666; font-size: 12px;'>AST + Symbols được chuyển đến Interpreter</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    # ---- STEP 4: EXECUTION ----
    st.subheader("⚡ Bước 4: Execution (Thực thi)")
    
    if show_output:
        with st.container():
            st.markdown("""
            <div class="info-box">
                <strong>💡 Đây là bước cuối cùng!</strong><br>
                Interpreter duyệt qua AST và thực thi từng câu lệnh.<br>
                Kết quả được in ra console (output).
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("📥 **Input:** AST + Symbol Table")
            st.caption("⚙️ **Process:** Interpretation - thực thi từng node")
            st.caption("📤 **Output:** Program output")
            
            if state.output:
                st.markdown("""
                <div class="success-box">
                    <strong>✅ Thực thi thành công!</strong>
                </div>
                """, unsafe_allow_html=True)
                st.code(state.output, language="text")
            elif state.errors:
                st.markdown("""
                <div class="error-box">
                    <strong>❌ Có lỗi xảy ra:</strong>
                </div>
                """, unsafe_allow_html=True)
                for error in state.errors:
                    st.code(error, language="text")
            else:
                st.info("Chưa có output. Nhấn 'Run' để thực thi.")
    else:
        st.info("Bật 'Hiển thị Output' trong sidebar để xem")

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
