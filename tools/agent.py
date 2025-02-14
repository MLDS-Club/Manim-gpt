from langchain.agents import AgentExecutor, create_tool_calling_agent
from googleAI import llm
from manimDocret import manimSearch
from langchain_core.prompts import ChatPromptTemplate

tools = [manimSearch]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant that generates code for a manim script that can solve a math problem."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "How do I draw a hexagon?"})
print(result["output"])