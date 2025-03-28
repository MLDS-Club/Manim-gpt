from langchain.agents import AgentExecutor, create_tool_calling_agent
from .googleAI import llm
from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate

tools = [manimSearch, executeManim]

print("== Initializing agent with tools ... ==")

# Refined system prompt emphasizing Manim 0.19.0 compatibility and final code correctness
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a mathematical visualization assistant. Follow these steps carefully:

1. Analyze the user's math problem or question.
2. Use the "manimSearch" tool to look up relevant documentation or techniques from Manim. 
3. Generate Python code using Manim that:
   - Solves/explains the problem mathematically.
   - Creates clear, instructive visual animations for each step.
   - Uses only methods and syntax compatible with Manim Community version 0.19.0. 
     For example:
       - Use Sector(radius=...) instead of outer_radius.
       - Do not pass 'direction' or 'buff' directly into VGroup(...).
       - Only use features guaranteed to exist in 0.19.0.
4. Always use the "executeManim" tool to test the code. If any syntax errors appear, fix them
   by generating new code and retesting. Repeat until it is correct for Manim 0.19.0.
5. No disclaimers, no extraneous commentary. Return ONLY the final working code in a single
   Python code block once all fixes are complete.
6. The final code must render without errors and produce a valid mp4 when run with Manim 0.19.0.
7. Keep all text and animations relevant to solving or explaining the user's request.
8. Do not show your reasoning or scratchpad. Return the final answer in code form only.

Remember: 
 - 'manimSearch' can be used to find official documentation for older versions of Manim if needed.
 - 'executeManim' must be used to verify correctness before finalizing the code.
"""
    ),
    ("user", "{input}"),
    # The "assistant" role for the chain-of-thought / scratchpad
    ("assistant", "{agent_scratchpad}")
])

# Create the agent with the revised prompt
agent = create_tool_calling_agent(llm, tools, prompt)
agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def createScript(request):
    print(f"Executing agent with request: {request}")
    # The agent will produce the final manim code, having tested it with executeManim
    return agentExecutor.invoke({"input": request})["output"]

print("== Agent created successfully. Ready to process requests. ==")

if __name__ == "__main__":
    math_problem = "How do I solve for the determinant of a 3x3 matrix?"
    result = agentExecutor.invoke({"input": math_problem})
    print(result)
