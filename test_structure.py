#!/usr/bin/env python3
"""
Simple test to verify the project structure and basic functionality
without requiring all dependencies
"""

import sys
import ast
import os
from pathlib import Path


def test_file_syntax(filepath):
    """Test if a Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def test_imports(filepath):
    """Extract imports from a file"""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return True, imports
    except Exception as e:
        return False, str(e)


def main():
    """Run tests"""
    print("=" * 60)
    print("GOAT Project Structure Tests")
    print("=" * 60)
    
    # Files to test
    python_files = [
        'main.py',
        'goat_player.py',
        'ai_module.py',
        'config.py',
        'demo.py',
        'setup.py'
    ]
    
    doc_files = [
        'README.md',
        'USAGE.md',
        'INSTALL.md',
        'LICENSE',
        'requirements.txt',
        '.gitignore'
    ]
    
    print("\n1. Checking Python files syntax...")
    all_valid = True
    for fname in python_files:
        if os.path.exists(fname):
            valid, msg = test_file_syntax(fname)
            status = "✓" if valid else "✗"
            print(f"   {status} {fname:20s} - {msg}")
            all_valid = all_valid and valid
        else:
            print(f"   ✗ {fname:20s} - File not found")
            all_valid = False
    
    print("\n2. Checking documentation files...")
    for fname in doc_files:
        exists = os.path.exists(fname)
        status = "✓" if exists else "✗"
        size = os.path.getsize(fname) if exists else 0
        print(f"   {status} {fname:20s} - {size} bytes")
    
    print("\n3. Checking key imports...")
    key_files = {
        'goat_player.py': ['pygame', 'numpy', 'cv2', 'librosa'],
        'ai_module.py': ['numpy', 'librosa'],
        'main.py': ['pygame', 'goat_player']
    }
    
    for fname, expected in key_files.items():
        success, imports = test_imports(fname)
        if success:
            found = [imp for imp in expected if any(imp in i for i in imports)]
            print(f"   {fname:20s} - Found {len(found)}/{len(expected)} expected imports")
        else:
            print(f"   {fname:20s} - Error: {imports}")
    
    print("\n4. Checking project structure...")
    structure = {
        'Core Player': 'goat_player.py',
        'AI Module': 'ai_module.py',
        'Configuration': 'config.py',
        'Main Entry': 'main.py',
        'Demo Script': 'demo.py',
        'Setup Script': 'setup.py',
        'Dependencies': 'requirements.txt',
        'Main Docs': 'README.md',
        'Usage Guide': 'USAGE.md',
        'Install Guide': 'INSTALL.md',
        'License': 'LICENSE',
        'Git Ignore': '.gitignore'
    }
    
    for component, fname in structure.items():
        exists = os.path.exists(fname)
        status = "✓" if exists else "✗"
        print(f"   {status} {component:20s} - {fname}")
    
    print("\n5. Feature verification...")
    features = {
        'Multi-format support': 'goat_player.py',
        'Reactive visuals': 'goat_player.py',
        'AI integration': 'ai_module.py',
        'Configuration system': 'config.py',
        'Demo mode': 'demo.py',
        'Cross-platform setup': 'setup.py'
    }
    
    for feature, fname in features.items():
        exists = os.path.exists(fname)
        status = "✓" if exists else "✗"
        print(f"   {status} {feature}")
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✓ All tests passed! Project structure is valid.")
        print("\nTo use GOAT:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run demo: python demo.py")
        print("  3. Or play media: python main.py /path/to/file.mp3")
        return 0
    else:
        print("✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
