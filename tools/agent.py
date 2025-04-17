from langchain.agents import AgentExecutor, create_tool_calling_agent
from .googleAI import llm
from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate

tools = [manimSearch, executeManim]

print("== Initializing agent with tools ... ==")

# UPDATED PROMPT: We renamed ("placeholder", ...) to ("assistant", ...)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a mathematical visualization assistant. Follow these steps:
1. Analyze the user's math problem
2. ALWAYS Use manimSearch to find relevant Manim documentation/techniques before generating your solution
3. Generate Python code using Manim that:
   - Solves the problem mathematically
   - Creates visual animations explaining each step
   - Uses appropriate Manim components (Scenes, MObjects, Animations)
4. Use executeManim to test the code and ensure it works correctly, ALWAYS use this tool.
6. MAKE SURE EVERYTHING WORKS, no errors should occur when rendering the code into an mp4
5. Return ONLY the final code in proper Manim format
7. Make sure to declare all variables, there should be no "undefined" errors
8. Make sure everything stays in frame when genorating the manim code. 
9. If manimsearch is NOT CALLED THE CODE WILL THROW AN ERROR.

When creating your code, you should create visually informative graphics. In doing so, please follow the rules below:
1. Make sure that all elements on the screen are clearly visible to the viewer and not overlapping with other elements unless necessary for visual explanation.
2. When moving between multiple steps of a solution, use clear transitions and animations of objects.
3. Never include animations, objects, text, or other elements that are irrelevant to the solution of the problem.

While coming up with your solution, you should always call the agent tool "manimSearch" to search for relevant Manim documentation.
"""),
    ("user", "{input}"),
    # The "agent_scratchpad" must remain in the prompt, but we rename the role to "assistant"
    ("assistant", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def createScript(request):
    print(f"Executing agent with request: {request}")
    return agentExecutor.invoke({"input": request})["output"]

print("== Agent created successfully. Ready to process requests. ==")

if __name__ == "__main__":
    math_problem = "How do I solve for the determinant of a 3x3 matrix?"
    result = agentExecutor.invoke({"input": math_problem})
    print(result)
