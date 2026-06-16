"""
TOPIC: LCEL (LangChain Expression Language) - modern pipe (|) style

CONCEPT:
Ye 2026 me LangChain ka recommended tareeka hai chains banane ka -
"|" operator se Runnable pieces ko jodte ho. Pichli files (LLMChain,
SequentialChain) "legacy" style thi - ab chalti hain, par naye
projects me LCEL likhna chahiye.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# --- Basic LCEL chain (jaise ek LLMChain ka replacement) ---
joke_prompt = PromptTemplate.from_template("Is topic par ek chhota joke banao: {topic}")
joke_chain = joke_prompt | llm | parser

print("Basic LCEL output:", joke_chain.invoke({"topic": "Programmers"}))


# --- Multi-step LCEL (SequentialChain (04 file) ka LCEL version) ---
title_prompt = PromptTemplate.from_template("Is topic ke liye catchy blog title banao: {topic}")
outline_prompt = PromptTemplate.from_template("Is blog title ke liye 4-point outline banao: {title}")
caption_prompt = PromptTemplate.from_template("Is outline se Twitter caption banao (under 280 chars): {outline}")

full_chain = (
    RunnablePassthrough.assign(title=title_prompt | llm | parser)
    .assign(outline=outline_prompt | llm | parser)
    .assign(caption=caption_prompt | llm | parser)
)

result = full_chain.invoke({"topic": "Machine Learning ke beginners ke liye tips"})
print("\n=== LCEL multi-step output ===")
print("Title:", result["title"])
print("\nOutline:", result["outline"])
print("\nCaption:", result["caption"])

# NOTICE: .assign() har step ka output dictionary me ADD karta jaata hai,
# bilkul SequentialChain ke output_key jaisa - bas naya syntax hai.


# --- Streaming dekho (LCEL ka bada fayda) ---
print("\n=== Streaming output (token-by-token) ===")
for chunk in joke_chain.stream({"topic": "Cats"}):
    print(chunk, end="", flush=True)
print()  # naya line end me


# ============================================
# TRY IT YOURSELF:
# 1. full_chain me ek 4th .assign() add karo: caption se "hashtags" banao.
# 2. joke_chain.batch([{"topic": "Dogs"}, {"topic": "Cats"}, {"topic": "Birds"}])
#    try karo - ye multiple inputs ek saath process karta hai (parallel-ish).
# 3. Socho aur likho: SequentialChain (legacy) aur ye RunnablePassthrough.assign()
#    style - dono me kya kaam same hai, syntax me kya farak hai?
# ============================================
