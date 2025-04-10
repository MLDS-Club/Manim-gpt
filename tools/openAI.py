# openAI.py

print("== Initializing OpenAI ChatGPT LLM ... ==")

from langchain_community.chat_models import ChatOpenAIForFunctions
from .dataLoader import getConfigKey

model_name = "gpt-3.5-turbo"

# This class should implement the needed .bind_tools(...) method
llm = ChatOpenAIForFunctions(
    model_name=model_name,
    temperature=0.5,
    openai_api_key=getConfigKey("openai_api_key"),
)

print("== ChatGPT LLM initialized successfully. ==")

if __name__ == "__main__":
    # Simple test
    response = llm.predict("Hello, world!")
    print("Test Prompt Response:", response)
