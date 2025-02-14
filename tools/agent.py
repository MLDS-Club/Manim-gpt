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
4. Return ONLY the final code in proper Manim format"""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

math_problem = "What is the length of the hypotenuse of a triangle with legs of length 3 and 4?"
result = agent_executor.invoke({"input": math_problem})
print(result["output"])