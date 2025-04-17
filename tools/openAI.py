from langchain_openai import ChatOpenAI
import os
import bs4
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from tools.dataLoader import getConfigKey

# ── CHANGE THIS to pick your model ──────────────────────────────────────────────
AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "o4-mini-2025-04-16",
    "gpt-4.1-2025-04-14",
    #"gpt-4o-2024-08-06",
    "gpt-4o",
    "text-davinci-003"
]
MODEL_INDEX = 3  # 0 → gpt-3.5-turbo, 1 → gpt-4, etc.
# ────────────────────────────────────────────────────────────────────────────────

# Safely grab the model name
try:
    model_name = AVAILABLE_MODELS[MODEL_INDEX]
except IndexError:
    raise ValueError(
        f"MODEL_INDEX {MODEL_INDEX} out of range; "
        f"choose 0–{len(AVAILABLE_MODELS)-1}"
    )

print(f"== Initializing {model_name} LLM ... ==")

llm = ChatOpenAI(
    model=model_name,
    temperature=1,
    openai_api_key=getConfigKey("openai_api_key"),
)

print(f"== {model_name} LLM initialized successfully. ==")

if __name__ == "__main__":
    print(llm.invoke("What company developed you?"))
