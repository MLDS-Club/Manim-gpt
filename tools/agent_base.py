# File: agent_base.py
from langchain.agents import AgentExecutor, create_tool_calling_agent
from .googleAI import llm
from .manimDocret import manimSearch
from .manimCodeTester import executeManim
from langchain_core.prompts import ChatPromptTemplate

class ManimAgent:
    """
    Core agent that uses LangChain to generate Manim-based mathematical visualizations.
    """
    def __init__(self):
        # Define available tools
        self.tools = [manimSearch, executeManim]

        # Build the system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are a mathematical visualization assistant. Always follow these steps:

1. FIRST, call the manimSearch tool with the user's request. Use exactly this JSON format (no markdown fences):
{"tool": "manimSearch", "tool_input": "<user request>"}

2. Wait for the returned documentation observation.
3. Analyze the user's math problem.
4. Generate Python code using Manim that:
   - Solves the problem mathematically
   - Creates visual animations explaining each step
   - Uses appropriate Manim components (Scenes, MObjects, Animations)
5. Use executeManim to test the code and ensure it works correctly.
6. MAKE SURE EVERYTHING WORKS; no errors should occur when rendering to mp4.
7. Return ONLY the final code in proper Manim format.
"""),
            ("user", "{input}"),
            ("assistant", "{agent_scratchpad}")
        ])

        # Create agent and executor
        self.agent = create_tool_calling_agent(llm, self.tools, prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def create_script(self, request: str) -> str:
        """
        Invoke the agent directly with the user's request.
        """
        print(f"[BaseAgent] Processing request: {request}")
        result = self.executor.invoke({"input": request})["output"]
        return result


if __name__ == "__main__":
    base = ManimAgent()
    print(base.create_script("How do I solve for the determinant of a 3x3 matrix?"))


# File: agent_prefetch.py
from .agent_base import ManimAgent
from .manimDocret import manimSearch

class PrefetchManimAgent(ManimAgent):
    """
    Subclass of ManimAgent that pre-fetches documentation on each request.
    """
    def __init__(self):
        super().__init__()

    def create_script(self, request: str) -> str:
        print(f"[PrefetchAgent] Pre-fetching docs for: {request}")
        # Retrieve relevant Manim documentation
        docs = manimSearch(request)
        docs_text = "\n".join(f"- {doc}" for doc in docs)
        # Prepend docs to the original request
        composite = f"Relevant Manim documentation:\n{docs_text}\n\n{request}"
        # Delegate to base implementation
        return super().create_script(composite)

if __name__ == "__main__":
    agent = PrefetchManimAgent()
    print(agent.create_script("How do I solve for the determinant of a 3x3 matrix?"))
