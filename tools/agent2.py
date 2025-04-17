from langchain.agents import AgentExecutor, create_tool_calling_agent
from .googleAI import llm
from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate

# Define available tools
tools = [manimSearch, executeManim]

print("== Initializing agent with tools ... ==")

# Core prompt for the agent
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a mathematical visualization assistant. Follow these steps:
1. Analyze the user's math problem
2. ALWAYS Use manimSearch to find relevant Manim documentation/techniques before generating your solution
3. Generate Python code using Manim that:
   - Solves the problem mathematically
   - Creates visual animations explaining each step
   - Uses appropriate Manim components (Scenes, MObjects, Animations)
4. Use executeManim to test the code and ensure it works correctly, ALWAYS use this tool.
5. MAKE SURE EVERYTHING WORKS; no errors should occur when rendering the code into an mp4
6. Return ONLY the final code in proper Manim format
7. Declare all variables to avoid undefined errors
8. Ensure everything stays in frame when generating the Manim code
9. If manimSearch is NOT called before code generation, the code will throw an error.
"""),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# Create the tool-calling agent and executor
agent = create_tool_calling_agent(llm, tools, prompt)
agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def createScript(request: str) -> str:
    """
    Always fetch relevant documentation before invoking the agent,
    ensuring manimSearch is called on every request.
    """
    print(f"Executing agent with request: {request}")
    # Pre-fetch relevant Manim documentation
    docs = manimSearch(request)
    # Format the retrieved passages
    docs_text = "\n".join(f"- {doc}" for doc in docs)
    # Prepend docs to the original user request
    composite_input = f"Relevant Manim documentation:\n{docs_text}\n\n{request}"
    # Invoke the agent with the composite input
    output = agentExecutor.invoke({"input": composite_input})["output"]
    return output

print("== Agent created successfully. Ready to process requests. ==")

if __name__ == "__main__":
    math_problem = "How do I solve for the determinant of a 3x3 matrix?"
    result = createScript(math_problem)
    print(result)
