from langchain_unstructured import UnstructuredLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4

loader = WebBaseLoader(
    web_paths=(url,),
    # bs_kwargs=dict(
    #     parse_only=bs4.SoupStrainer(
    #         class_=("<p>")
    #     )
    # ),
)
docs = loader.load()

from bs4 import BeautifulSoup
import urllib.request
urls = []
pages = []
visited = {""}
# function add_page(url):
#     pass

def all_hrefs(href):
    return href and not "#" in href and href.startswith("reference")

def url_to_text(url):
    try:
      fp = urllib.request.urlopen(url)
    except:
      return
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(mystr)
    for code in soup.find_all(class_="pre"):
        if code.string:
          code.string.replace_with("`"+code.string+"`")
          if "[source]" in code.string:
              code.string.replace_with("")

    for code in soup.find_all("pre"):
        if code.string:
          code.decompose()

    for code in soup.find_all(class_="highlight"):
        for pre in code.find_all("pre"):
            spans = pre.find_all("span")
            # print(spans)
            first_span = spans[1]
            last_span = spans[-1]
            if first_span.string and last_span.string:
                first_span.string.replace_with("`"+first_span.string)
                last_span.string.replace_with(last_span.string+"`")

    urls.append(url)
    pages.append(soup.article.get_text())

    soup = soup.article

    links = soup.find_all(href=all_hrefs)
    for link in links:
        link["href"] = "https://docs.manim.community/en/stable/" + link["href"]
        if link["href"] not in visited:
            visited.add(link["href"])
            url_to_text(link["href"])

visited.add("https://docs.manim.community/en/stable/reference.html")
url_to_text("https://docs.manim.community/en/stable/reference.html")
print(urls)

import chromadb
import chromadb.utils.embedding_functions as embedding_functions
# from google.colab import userdata
# from torch

# hf_api = userdata.get("huggingface")
huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="NovaSearch/stella_en_1.5B_v5",
    device = "cuda"
)
chroma_client = chromadb.PersistentClient(path="./manim")
collection = chroma_client.create_collection(name="manim_docs2801", embedding_function=huggingface_ef)
ids = urls
collection.add(documents=pages, ids=ids)
