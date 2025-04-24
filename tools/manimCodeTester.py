import ast
import subprocess
import tempfile
import traceback
import os
import sys
import py_compile

from langchain_core.tools import tool

@tool
def executeManim(code: str, timeout: int = 40) -> dict:
    """
    Executes a Manim scene for syntax and runtime validation by invoking the Manim CLI.
    Falls back to a Python import check if no Scene subclass is detected.

    Returns:
        dict: {"success": bool, "output": str, "error": str}
    """
    # 1) Top-level Python syntax check
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return {"success": False, "output": "", "error": f"SyntaxError: {e}"}

    # 2) Detect Scene subclasses via AST
    scene_names = []
    try:
        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_id = getattr(base, 'id', None) or getattr(base, 'attr', None)
                    if isinstance(base, (ast.Name, ast.Attribute)) and base_id and base_id.endswith('Scene'):
                        scene_names.append(node.name)
    except Exception:
        # if AST parse fails, we'll fallback to import check below
        pass

    temp_filename = None
    try:
        # 3) Write code to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(code)
            temp_filename = temp_file.name

        # 4) Optional: byte-compile check
        try:
            py_compile.compile(temp_filename, doraise=True)
        except py_compile.PyCompileError as e:
            os.remove(temp_filename)
            return {"success": False, "output": "", "error": f"CompileError: {e}"}

        # 5) Build command: Manim CLI if scene found, else plain Python import
        if scene_names:
            cmd = ["manim", "-ql", temp_filename] + scene_names
        else:
            cmd = [sys.executable, temp_filename]

        # 6) Run and enforce success via check=True
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        # Clean up
        os.remove(temp_filename)
        return {"success": True, "output": result.stdout.strip(), "error": ""}

    except subprocess.CalledProcessError as e:
        # Catch CLI or import errors
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return {
            "success": False,
            "output": e.stdout.strip(),
            "error": e.stderr.strip() or f"Exited with code {e.returncode}"
        }
    except subprocess.TimeoutExpired:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return {"success": False, "output": "", "error": "Error: Execution timed out."}
    except Exception:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return {"success": False, "output": "", "error": traceback.format_exc()}