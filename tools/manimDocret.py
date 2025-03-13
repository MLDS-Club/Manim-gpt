from langchain_core.tools import tool
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import torch
from pathlib import Path

# Get the script's directory - this way the file can be ran from anywhere
script_dir = Path(__file__).parent
# Construct the path relative to the script and resolve it to an absolute path
data_path = script_dir / ".." / "data" / "manim"
manimPath = str(data_path.resolve())

device = "cuda"
if not torch.cuda.is_available():
  print("Warning: CUDA (NVIDIA GPU) is not available to run manimSearch. Using CPU instead.")
  device = "cpu"


#Run this on startup to load the model and collection so it doesn't have to be done every time -- this is all essentially part of the function below
huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="NovaSearch/stella_en_1.5B_v5",
    device = device, # xla for TPU, cuda for GPU, cpu for CPU (still have to get xla to work but cuda takes ~1 second or less, cpu takes ~30 seconds per query)
    trust_remote_code=True
)
chromaClient = chromadb.PersistentClient(path=manimPath)
collection = chromaClient.get_collection("manim_docs2801", embedding_function=huggingface_ef)

@tool 
def manimSearch(query:str) -> list:
  """
  Retrieve information from manim documentation to perform task, the query should be as if it is a web search within documentation. 
  Returns a list of 15 relevant string passages.
  """
  queryPrompt = f"Given a web search query, retrieve relevant passages that answer the query '{query}'"
  return collection.query(query_texts=queryPrompt, n_results=15)["documents"][0] #index 0 gets the list

if __name__ == "__main__":
  print(manimSearch.invoke("How to create a circle in manim?")[0])
  #print(manimSearch.invoke("How to create a circle in manim?"))