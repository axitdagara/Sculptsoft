"""
TOPIC: Classes / OOP - LangChain me sab "Runnable" class kyun hain

CONCEPT:
LangChain ke andar ChatOpenAI, PromptTemplate, StrOutputParser - ye sab
DIFFERENT classes hain, lekin sabka ek COMMON base hai: "Runnable".

Iska matlab: sab ke paas same methods hote hain -> .invoke(), .batch(), .stream()
Isi wajah se tum unko "|" (pipe) operator se jod paate ho - kyunki har piece
ek hi "interface" follow karta hai.
"""

from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda

load_dotenv() # .env file se saari keys load karega

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")
prompt = ChatPromptTemplate.from_template("Ek line me bata: {topic}")
parser = StrOutputParser()

# Check karo: ye sab Runnable hain ya nahi
print("llm Runnable hai?", isinstance(llm, Runnable))
print("prompt Runnable hai?", isinstance(prompt, Runnable))
print("parser Runnable hai?", isinstance(parser, Runnable))

# Isi wajah se teeno same tarah .invoke() karte hain:
print("\n--- Har ek alag se invoke ---")
formatted_prompt = prompt.invoke({"topic": "Python"})
print(type(formatted_prompt))  # ChatPromptValue object

# Aur isi wajah se "|" se chain bana sakte ho (sab Runnable hone ki wajah se)
chain = prompt | llm | parser
result = chain.invoke({"topic": "Python"})
print("\nChain ka output:", result)

# Tum khud bhi apna ek "custom Runnable" bana sakte ho ek normal function se:
def shout(text: str) -> str:
    return text.upper() + "!!!"

custom_step = RunnableLambda(shout)
full_chain = prompt | llm | parser | custom_step
print("\nCustom Runnable ke saath:", full_chain.invoke({"topic": "Python"}))


# ============================================
# TRY IT YOURSELF:
# 1. isinstance() check karo `custom_step` ke liye bhi - kya wo bhi Runnable hai?
# 2. Apna ek custom function bana jo text ko reverse kare, aur chain me add karo.
# 3. print(type(llm)) aur print(type(prompt)) karke dekho exact class names kya hain.
# ============================================
