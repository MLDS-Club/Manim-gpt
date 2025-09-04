# Manim-gpt

An AI-powered pipeline that turns plain-English prompts into Manim Community animations. It pulls tips from a local Manim doc index via RAG, drafts a storyboard, then writes, self-tests, and renders the scene—dropping the script and MP4 into /output. Built on LangChain tool-calling (OpenAI or Gemini), a ChromaDB retriever, and an optional two-phase creator→executor agent.

One-shot agent (agent.py) or two-phase “creator → executor” flow (agent_doublehead.py)

manimSearch: ChromaDB + local embeddings to surface relevant Manim usage patterns

executeManim: runs the CLI to catch syntax/runtime issues before finalizing

scriptToVideo.py: cleans, renders, and moves the newest MP4 to /output/compiledVideo

Swappable LLMs (OpenAI/Gemini) behind a simple LangChain interface
