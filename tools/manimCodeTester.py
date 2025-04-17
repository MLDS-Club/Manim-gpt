import subprocess
import tempfile
import traceback
import os
import sys
import re
from langchain_core.tools import tool

@tool
def executeManim(code: str, timeout: int = 10) -> dict:
    """
    Executes a Manim scene for syntax and runtime validation by invoking the Manim CLI.
    Falls back to a Python import check if no Scene subclass is detected.

    Args:
        code (str): The Python code containing the Manim script.
        timeout (int): Max time (in seconds) before forcefully stopping execution.

    Returns:
        dict: {"success": bool, "output": str, "error": str}
    """
    temp_filename = None
    try:
        # 1) Write out the code to a UTF-8 file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".py",
            mode="w",
            encoding="utf-8"
        ) as temp_file:
            temp_file.write(code)
            temp_filename = temp_file.name

        # 2) Detect a Scene subclass name via regex
        match = re.search(r"class\s+(\w+)\s*\(.*Scene.*\)", code)
        if match:
            scene_name = match.group(1)
            # 3) Invoke Manim CLI in low-quality mode for fast validation
            cmd = [
                "manim",
                "-ql",            # low quality, fastest
                temp_filename,
                scene_name
            ]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout
            )
        else:
            # Fallback: simple Python import check
            process = subprocess.run(
                [sys.executable, temp_filename],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout
            )

        # 4) Cleanup temp file
        os.remove(temp_filename)
        temp_filename = None

        # 5) Return structured result
        if process.returncode == 0:
            return {"success": True, "output": process.stdout.strip(), "error": ""}
        else:
            return {"success": False, "output": "", "error": process.stderr.strip()}

    except subprocess.TimeoutExpired:
        # Ensure temp file is removed if created
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return {"success": False, "output": "", "error": "Error: Execution timed out."}

    except Exception:
        # Catch-all for unexpected errors
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return {"success": False, "output": "", "error": traceback.format_exc()}

# Example Usage (Standalone Testing)
if __name__ == "__main__":
    sample_code = '''
from manim import *

class HexagonScene(Scene):
    def construct(self):
        hexagon = Polygon(
            UP, UP+RIGHT, RIGHT, DOWN, DOWN+LEFT, LEFT
        )
        self.play(Create(hexagon))
        self.wait(2)
'''
    result = executeManim(sample_code)
    if result["success"]:
        print("\n✅ Execution Successful:\n", result["output"])
    else:
        print("\n❌ Execution Failed:\n", result["error"])
