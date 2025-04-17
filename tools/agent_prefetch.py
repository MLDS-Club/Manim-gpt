
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
