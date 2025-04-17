# agent.py

from langchain.agents import AgentExecutor, create_tool_calling_agent
# Import from the updated openAI.py file that uses ChatOpenAIForFunctions
from .openAI import llm
#from .googleAI import llm

from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate

tools = [manimSearch, executeManim]

print("== Initializing agent with tools ... ==")

# System prompt emphasizing Manim 0.19.0 compatibility
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a mathematical visualization assistant powered by Manim Community v0.19.0. Follow these rules exactly:

0. **Always Invoke manimSearch**  
   - Before writing any code, call the `manimSearch` tool to gather relevant docs, examples, and inspiration.  
   - Use what you find to craft the most **informative**, **interesting**, and **beautiful** graphic possible.

1. **Scene Detection**  
   - Parse the user’s request and decide on one `Scene` subclass name.  
   - Your final code must define exactly one `class Foo(Scene): construct(self): ...`.

2. **Use First‑Class Path APIs**  
   - **Never** do `VMobject().set_points_as_cubic_bezier(...)` without capturing its return value.  
   - **Always** use `CubicBezier(start, ctrl1, ctrl2, end)` or:
     ```python
     path = VMobject().set_points_as_cubic_bezier([...])
     ```  
   - This guarantees each `path` has non‑empty `.points`.

3. **Tool‑Driven Validation Loop**  
   - After writing the scene code, **always** call the `executeManim` tool to fully render in low‑quality mode (`manim -ql`), catching syntax *and* runtime errors.  
   - If `executeManim` returns `success=False`, fix the code *and* re‑invoke it. Repeat until there are no errors.

4. **No Extraneous Output**  
   - Do **not** include your reasoning or intermediate logs in the final output.  
   - Return **only** the complete, final working Python code block.

5. **Manim 0.19.0 Compatibility**  
   - Use only APIs guaranteed in 0.19.0 (e.g. `Sector(radius=…)`, not `outer_radius`).  
   - Avoid deprecated parameters (don’t pass `direction` or `buff` directly to `VGroup`).

6. **Final Delivery**  
   - Once `executeManim` passes, output exactly one Python file’s contents that, when run, produces a valid MP4 without errors.
"""),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# Create the agent with the revised prompt
agent = create_tool_calling_agent(llm, tools, prompt)
agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def createScript(request):
    print(f"Executing agent with request: {request}")
    return agentExecutor.invoke({"input": request})["output"]

print("== Agent created successfully. Ready to process requests. ==")

if __name__ == "__main__":
    test_question = "How do I solve for the determinant of a 3x3 matrix?"
    result = agentExecutor.invoke({"input": test_question})
    print(result)
