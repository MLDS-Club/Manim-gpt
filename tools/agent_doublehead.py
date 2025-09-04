# agent.py  ── two-phase Manim agent (creator + executor)

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate

# Updated OpenAI wrapper that supports tool calls
from .openAI import llm   # noqa: E402

# Tools
from .manimDocret import manimSearch          # noqa: E402
from .manimCodeTester import executeManim     # noqa: E402
from tools import prompts                     # noqa: E402

# ---------------------------------------------------------------------------
# Helper: capture every tool the agent invokes
# ---------------------------------------------------------------------------
class ToolTracker(BaseCallbackHandler):
    """Collects the names of all tools used during an Agent run."""
    def __init__(self) -> None:
        self.used_tools: list[str] = []

    def on_tool_start(self, *args, **kwargs):
        # args[0] might be the tool name or dict, inspect to confirm
        serialized = args[0]
        name = serialized.get("name", "<unknown>")
        self.used_tools.append(name)


# ---------------------------------------------------------------------------
# Stage 1 – storyboard creator
# ---------------------------------------------------------------------------
creator_tools = [manimSearch]  # ONLY storyboard-safe tools
creator_prompt: ChatPromptTemplate = prompts.a2_create_tasks

creator_agent = create_tool_calling_agent(llm, creator_tools, creator_prompt)
creator_executor = AgentExecutor(
    agent=creator_agent,
    tools=creator_tools,
    verbose=False   # keep console clean – we’ll print what we need
)

# ---------------------------------------------------------------------------
# Stage 2 – code executor
# ---------------------------------------------------------------------------
executor_tools = [executeManim, manimSearch]  # may re-query docs, then render
executor_prompt: ChatPromptTemplate = prompts.a2_execute_tasks

executor_agent = create_tool_calling_agent(llm, executor_tools, executor_prompt)
executor_executor = AgentExecutor(
    agent=executor_agent,
    tools=executor_tools,
    verbose=False
)

# ---------------------------------------------------------------------------
# Public façade (same name as before)
# ---------------------------------------------------------------------------
def createScript(request: str) -> str:
    """Generate storyboard + Manim code, printing diagnostics as required."""
    # ---- Stage 1 ----------------------------------------------------------
    creator_tracker = ToolTracker()
    storyboard = creator_executor.invoke(
        {"storyboard": "", "input": request},  # extra key for prompt var
        config={"callbacks": [creator_tracker]}
    )["output"]

    print("\n===== STORYBOARD (Stage 1 output) =====")
    print(storyboard)                 # Print the storyboard itself
    print("===== TOOLS USED IN STAGE 1 =====")
    for tname in creator_tracker.used_tools:
        print(f"- {tname}")
    print("=======================================\n")

    # ---- Stage 2 ----------------------------------------------------------
    executor_tracker = ToolTracker()
    script_output = executor_executor.invoke(
        {"storyboard": storyboard},
        config={"callbacks": [executor_tracker]}
    )["output"]

    # count lines in returned Python code
    n_lines = script_output.count("\n") + 1
    print(f"===== Stage 2 script length: {n_lines} lines =====\n")
    for tname in executor_tracker.used_tools:
        print(f"- {tname}")
    print("=======================================\n")

    # (Optional) list tools Stage 2 used — not part of the spec but handy
    # for debugging; comment out if undesired.
    # print("===== TOOLS USED IN STAGE 2 =====")
    # for tname in executor_tracker.used_tools:
    #     print(f"- {tname}")
    # print("===================================\n")

    return script_output  # returned identically to the old agent


# ---------------------------------------------------------------------------
# CLI test harness
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_question = "How do I solve for the determinant of a 3×3 matrix?"
    result_script = createScript(test_question)
    print("===== FINAL MANIM SCRIPT (returned value) =====")
    print(result_script)
