from langchain_core.tools import tool
import chromadb.utils.embedding_functions as embedding_functions
@tool 
def manim_search(query:str) -> list:
  """
  retrieve information from manim documentation to perform task, the quesry should be as if it is a web search within documentation. 
  """
  query_prompt = f"Given a web search query, retrieve relevant passages that answer the query '{query}'"
  huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="NovaSearch/stella_en_1.5B_v5",
      device = "cuda", # xla for TPU, cuda for GPU, cpu for CPU (still have to get xla to work but cuda takes ~1 second or less, cpu takes ~30 seconds per query)
      trust_remote_code=True
  )
  chroma_client = chromadb.PersistentClient(path="./manim")
  collection = chroma_client.get_collection("manim_docs2801", embedding_function=huggingface_ef)
  return collection.query(query_texts=query_prompt, n_results=15)["documents"]

