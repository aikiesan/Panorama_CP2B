"""
Fix syntax errors in migrated files by checking and adding missing closing brackets
"""

import ast
from pathlib import Path

def check_and_fix_file(file_path: Path):
    """Check if file has syntax errors and try to fix"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Try to parse
        ast.parse(code)
        print(f"OK: {file_path}")
        return True

    except SyntaxError as e:
        print(f"Error in {file_path}: {e}")

        # Try to fix common issues
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check if it's missing closing bracket
        if "was never closed" in str(e):
            print(f"  -> Attempting to fix by adding closing bracket...")

            # Add closing bracket
            if "(" in str(e):
                lines.append(")\n")
            elif "[" in str(e):
                lines.append("]\n")
            elif "{" in str(e):
                lines.append("}\n")

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            print(f"  -> Fixed! Re-checking...")
            return check_and_fix_file(file_path)

        return False

# Check all Python files in data folders
data_dir = Path('src/data')
for py_file in data_dir.rglob('*.py'):
    if py_file.name != '__pycache__':
        check_and_fix_file(py_file)

print("\nDone!")
