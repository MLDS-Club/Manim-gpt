from langchain.agents import AgentExecutor, create_tool_calling_agent
from googleAI import llm
from manimDocret import manimSearch
from langchain_core.prompts import ChatPromptTemplate

tools = [manimSearch]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a mathematical visualization assistant. Follow these steps:
1. Analyze the user's math problem
2. Use manimSearch to find relevant Manim documentation/techniques
3. Generate Python code using Manim that:
   - Solves the problem mathematically
   - Creates visual animations explaining each step
   - Uses appropriate Manim components (Scenes, MObjects, Animations)
4. Return ONLY the final code in proper Manim format
     
When creating your code, you should create visually informative graphics. In doing so, please follow the rules below:
1. Make sure that all elements on the screen are clearly visible to the viewer and not overlapping with other elements unless necessary for visual explanation.
2. When moving between multiple steps of a solution, use clear transitions and animations of objects.
3. Never include animations, objects, text, or other elements that are irrelevant to the solution of the problem."""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

math_problem = "What is 1 + 4?"
result = agent_executor.invoke({"input": math_problem})
f = open("./output/videoScript/manimOutput.py", "w")
f.write(result["output"])