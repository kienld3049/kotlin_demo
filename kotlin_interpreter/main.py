#!/usr/bin/env python3
"""
Kotlin Interpreter - Main Entry Point

Demo mô phỏng quá trình biên dịch và thực thi Kotlin từ A đến Z.
"""

import argparse
from pathlib import Path

from src.lexer import Lexer, Token
from src.parser import Parser
from src.semantic import ErrorCollector, SymbolTable, CollectionPass
from src.runtime import Evaluator


def print_header(title: str):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_step(step: str, description: str):
    """Print step information."""
    print(f"[{step}] {description}")
    print("-" * 70)


def demo_full_pipeline(source_code: str, show_details: bool = True):
    """
    Mô phỏng toàn bộ quá trình từ A đến Z như Gemini đã giải thích.
    
    A. Soạn thảo (Writing)
    B. Phân tích Từ vựng (Lexical Analysis)
    C. Phân tích Cú pháp (Syntax Analysis)
    D. Phân tích Ngữ nghĩa (Semantic Analysis)
    E. Sinh mã (Code Generation) - SIMPLIFIED: Thay vì sinh bytecode, ta sẽ
       sử dụng AST trực tiếp
    F. Thực thi (Execution) - Interpreter thay vì JVM
    """
    
    print_header("KOTLIN INTERPRETER - DEMO ĐẦY ĐỦ TỪ A → Z")
    
    # A. Soạn thảo
    print_step("A", "Soạn thảo (Writing)")
    print("Source code:")
    print(source_code)
    print()
    
    # B. Phân tích Từ vựng (Lexical Analysis)
    print_step("B", "Phân tích Từ vựng (Lexical Analysis - Lexer)")
    print("Chuyển đổi code thành các tokens (từ vựng)...")
    
    lexer = Lexer(source_code)
    
    try:
        tokens = lexer.tokenize()
    except Exception as e:
        print(f"❌ LỖI LEXER: {e}")
        return
    
    if show_details:
        print("\nTokens được tạo ra:")
        for i, token in enumerate(tokens[:20]):  # Show first 20 tokens
            print(f"  {i+1:3d}. {token.type:15s} : {repr(token.value)}")
        if len(tokens) > 20:
            print(f"  ... và {len(tokens) - 20} tokens nữa")
    else:
        print(f"✓ Tạo ra {len(tokens)} tokens")
    print()
    
    # C. Phân tích Cú pháp (Syntax Analysis)
    print_step("C", "Phân tích Cú pháp (Syntax Analysis - Parser)")
    print("Xây dựng cây cú pháp trừu tượng (AST)...")
    
    parser = Parser(tokens)
    
    try:
        ast = parser.parse()
        print(f"✓ AST được tạo với {len(ast.declarations)} declarations")
        
        if show_details:
            print("\nCấu trúc AST:")
            for i, decl in enumerate(ast.declarations):
                print(f"  {i+1}. {type(decl).__name__}")
                if hasattr(decl, 'name'):
                    print(f"     - name: {decl.name}")
    except Exception as e:
        print(f"❌ LỖI PARSER: {e}")
        return
    print()
    
    # D. Phân tích Ngữ nghĩa (Semantic Analysis)
    print_step("D", "Phân tích Ngữ nghĩa (Semantic Analysis)")
    print("Kiểm tra kiểu dữ liệu, phạm vi biến, v.v...")
    
    error_collector = ErrorCollector()
    symbol_table = SymbolTable()
    
    # Collection pass: Thu thập tất cả declarations
    collection_pass = CollectionPass(symbol_table, error_collector)
    collection_pass.collect(ast)
    
    if error_collector.has_errors():
        print("❌ LỖI NGỮ NGHĨA:")
        for error in error_collector.errors:
            print(f"  - {error}")
        return
    else:
        print("✓ Kiểm tra ngữ nghĩa thành công")
        if show_details:
            print("\nBảng ký hiệu (Symbol Table):")
            current_scope = symbol_table.current_scope
            for name, symbol in current_scope.symbols.items():
                print(f"  - {name}: {symbol.kind.value}")
    print()
    
    # E. Sinh mã (Code Generation)
    print_step("E", "Sinh mã (Code Generation)")
    print("SIMPLIFIED: Thay vì sinh Java Bytecode, ta sử dụng AST trực tiếp")
    print("(Trong Kotlin thực tế, bước này sẽ sinh ra file .class)")
    print("✓ AST sẵn sàng để thực thi")
    print()
    
    # F. Thực thi (Execution)
    print_step("F", "Thực thi (Execution)")
    print("Interpreter đang thực thi code...")
    print("-" * 70)
    
    evaluator = Evaluator()
    
    try:
        result = evaluator.evaluate(ast)
        print("-" * 70)
        print(f"✓ Thực thi thành công")
        if not result.type_name == "Unit":
            print(f"Kết quả: {result}")
    except Exception as e:
        print("-" * 70)
        print(f"❌ LỖI RUNTIME: {e}")
        import traceback
        if show_details:
            traceback.print_exc()
        return
    print()
    
    # Z. Kết quả
    print_step("Z", "Kết quả (Result)")
    print("Chương trình đã chạy xong!")
    print("Quá trình từ A → Z hoàn tất ✓")


def demo_step_by_step(source_code: str):
    """Demo từng bước riêng biệt."""
    
    print_header("DEMO TỪNG BƯỚC RIÊNG BIỆT")
    
    # Step 1: Lexer only
    print_step("1", "LEXER - Phân tích từ vựng")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(f"  Token: {token.type:15s} = {repr(token.value)}")
    
    input("\n[Nhấn Enter để tiếp tục sang PARSER...]")
    
    # Step 2: Parser only
    print_step("2", "PARSER - Phân tích cú pháp")
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("AST Structure:")
    for decl in ast.declarations:
        print(f"  - {type(decl).__name__}")
    
    input("\n[Nhấn Enter để tiếp tục sang EVALUATOR...]")
    
    # Step 3: Evaluator
    print_step("3", "EVALUATOR - Thực thi")
    evaluator = Evaluator()
    result = evaluator.evaluate(ast)
    print(f"\nKết quả: {result}")


def run_file(filepath: str, mode: str = "full"):
    """Run a Kotlin file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if mode == "full":
            demo_full_pipeline(source_code, show_details=True)
        elif mode == "step":
            demo_step_by_step(source_code)
        elif mode == "simple":
            demo_full_pipeline(source_code, show_details=False)
        elif mode == "run":
            # Just run without explanation
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            evaluator = Evaluator()
            evaluator.evaluate(ast)
    
    except FileNotFoundError:
        print(f"❌ File không tìm thấy: {filepath}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Kotlin Interpreter - Demo mô phỏng quá trình từ A → Z",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  full    - Hiển thị đầy đủ từng bước A→Z với chi tiết (mặc định)
  simple  - Hiển thị từng bước A→Z nhưng ít chi tiết hơn
  step    - Demo từng bước một, yêu cầu nhấn Enter để tiếp tục
  run     - Chỉ chạy code, không hiển thị quá trình

Examples:
  python main.py examples/hello_world.kt
  python main.py examples/hello_world.kt --mode step
  python main.py examples/arithmetic.kt --mode simple
        """
    )
    
    parser.add_argument('file', help='Kotlin source file to run')
    parser.add_argument(
        '--mode', '-m',
        choices=['full', 'simple', 'step', 'run'],
        default='full',
        help='Demo mode (default: full)'
    )
    
    args = parser.parse_args()
    
    run_file(args.file, args.mode)


if __name__ == "__main__":
    main()
