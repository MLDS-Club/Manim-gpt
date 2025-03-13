def manimSearch(
    query: str,
) -> dict:
  """Retrieve information from manim documentation to perform task, the query should be as if it is a web search within documentation. 
Returns a list of 15 relevant string passages.

  Args:
    query: 
  """


def executeManim(
    code: str,
    timeout: int | None = None,
) -> dict:
  """Only accepts isolated manim code. Executes a Manim script safely and captures errors. Should be used to check if a Manim script is valid after creating it.

Args:
    code (str): The Python code containing the Manim script.
    timeout (int): Max time (in seconds) before forcefully stopping execution.

Returns:
    dict: {"success": bool, "output": str, "error": str}

  Args:
    code: 
    timeout: 
  """