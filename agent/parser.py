import ast
from typing import List, Dict, Any
import os

def parse_file(file_path: str) -> List[Dict[str, Any]]:
    """Parses a Python file and extracts functions, classes, and imports."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return []
    
    chunks = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            # Extract function source
            try:
                func_source = ast.get_source_segment(source, node)
                if not func_source:
                    continue
                chunks.append({
                    "type": "function",
                    "name": node.name,
                    "file_path": file_path,
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "code": func_source
                })
            except Exception:
                pass
        elif isinstance(node, ast.ClassDef):
            try:
                class_source = ast.get_source_segment(source, node)
                if not class_source:
                    continue
                chunks.append({
                    "type": "class",
                    "name": node.name,
                    "file_path": file_path,
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "code": class_source
                })
            except Exception:
                pass
    
    return chunks
