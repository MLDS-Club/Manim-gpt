import subprocess
import tempfile
import traceback
import os
import sys
from langchain_core.tools import tool

@tool
def executeManim(code: str, timeout: int = 10) -> dict:
    """
    Only accepts isolated manim code. Executes a Manim script safely and captures errors. Should be used to check if a Manim script is valid after creating it.
    
    Args:
        code (str): The Python code containing the Manim script.
        timeout (int): Max time (in seconds) before forcefully stopping execution.
    
    Returns:
        dict: {"success": bool, "output": str, "error": str}
    """
    try:
        # Create a temporary file for the Manim script
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
            temp_file.write(code)
            temp_file.close()
            temp_filename = temp_file.name

        # Run the script using subprocess
        process = subprocess.run(
            [sys.executable, temp_filename],  # Uses the same Python interpreter
            capture_output=True,
            text=True,
            timeout=timeout  # Prevents infinite loops
        )

        # Cleanup the temporary file
        os.remove(temp_filename)

        # Check execution result
        if process.returncode == 0:
            return {"success": True, "output": process.stdout.strip(), "error": ""}
        else:
            return {"success": False, "output": "", "error": process.stderr.strip()}

    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "Error: Execution timed out."}

    except Exception as e:
        return {"success": False, "output": "", "error": traceback.format_exc()}


# Example Usage (Test it by running this script directly)
if __name__ == "__main__":
    sample_code = """
from manim import *

class HexagonScene(Scene):
    def construct(self):
        hexagon = Polygon(
            UP, UP+RIGHT, RIGHT, DOWN, DOWN+LEFT, LEFT
        )
        self.play(Create(hexagon))
        self.wait(2)
"""

    result = executeManim(sample_code)
    
    if result["success"]:
        print("\n✅ Execution Successful:\n", result["output"])
    else:
        print("\n❌ Execution Failed:\n", result["error"])