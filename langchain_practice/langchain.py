import os
os.environ["NVIDIA_API_KEY"] = "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"

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate


# Initialize the free hosted NIM model
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct", 
    temperature=0.7
)

# Invoke the model normally
response = llm.invoke("What are the benefits of using microservices?")
print(response.content)