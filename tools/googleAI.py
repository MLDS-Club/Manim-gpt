from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
import os
import bs4
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from dataLoader import getConfigKey

llm = ChatGoogleGenerativeAI(
	model="models/gemini-2.0-pro-exp-02-05",
	temperature=0.5,
	google_api_key= getConfigKey("google_api_key"),
	safety_settings={ 
		HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, 
		HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, 
		HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE}
)
 
if __name__ == "__main__":
    print(llm.invoke("What company developed you"))