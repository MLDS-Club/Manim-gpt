# agent.py

from langchain.agents import AgentExecutor, create_tool_calling_agent
# Import from the updated openAI.py file that uses ChatOpenAIForFunctions
from .openAI import llm
#from .googleAI import llm

from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate
from tools import prompts


tools = [manimSearch, executeManim]

print("== Initializing agent with tools ... ==")

# System prompt emphasizing Manim 0.19.0 compatibility
prompt = prompts.optimized2

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
