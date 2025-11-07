"""
Kotlin Interpreter - Streamlit Web GUI
Demo mô phỏng cách hoạt động của ngôn ngữ Kotlin từ A đến Z
"""

import streamlit as st
import pandas as pd
from src.gui.state_manager import StateManager
import json

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
                    "Type": token.type,
                    "Value": str(token.value),
                    "Line": token.line,
                    "Column": token.column
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
            
            def ast_to_dict(node):
                """Convert AST node to dict for display"""
                if node is None:
                    return None
                
                result = {
                    "type": node.__class__.__name__
                }
                
                # Add relevant attributes
                for attr in dir(node):
                    if not attr.startswith('_') and attr not in ['accept', 'visit']:
                        value = getattr(node, attr)
                        if not callable(value):
                            if isinstance(value, list):
                                result[attr] = [ast_to_dict(v) if hasattr(v, '__class__') and hasattr(v, 'accept') else str(v) for v in value]
                            elif hasattr(value, '__class__') and hasattr(value, 'accept'):
                                result[attr] = ast_to_dict(value)
                            else:
                                result[attr] = str(value)
                
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
            
            # Functions
            if state.symbol_table.functions:
                st.write("**Functions:**")
                func_data = []
                for name, func_info in state.symbol_table.functions.items():
                    func_data.append({
                        "Name": name,
                        "Return Type": str(func_info.get('return_type', 'Unit')),
                        "Parameters": str(func_info.get('params', []))
                    })
                if func_data:
                    st.dataframe(pd.DataFrame(func_data), use_container_width=True, hide_index=True)
            
            # Variables
            if hasattr(state.symbol_table, 'scopes') and state.symbol_table.scopes:
                st.write("**Variables (Global Scope):**")
                var_data = []
                for name, var_info in state.symbol_table.scopes[0].items():
                    if isinstance(var_info, dict):
                        var_data.append({
                            "Name": name,
                            "Type": str(var_info.get('type', 'Unknown')),
                            "Mutable": "var" if var_info.get('mutable', False) else "val"
                        })
                if var_data:
                    st.dataframe(pd.DataFrame(var_data), use_container_width=True, hide_index=True)
            
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
