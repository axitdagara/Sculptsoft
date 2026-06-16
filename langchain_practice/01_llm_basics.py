"""
TOPIC: LLM - model ko call karna

CONCEPT:
ChatOpenAI ek "wrapper" class hai jo OpenAI ke raw API ko LangChain ke
common interface me convert karta hai. Tum isko ek object banakar use karte ho.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# temperature=0    -> deterministic, factual jawab (kam creative)
# temperature=0.7  -> balanced
# temperature=1+   -> zyada creative/random
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Direct invoke - simple string bhejo
response = llm.invoke("Mujhe LangChain ke baare me 2 line me batao")
print("Response object:", response)
print("\nSirf text:", response.content)


print("\n--- Temperature ka effect dekho ---")
creative_llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.2)
factual_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

q = "Ek line me, baarish ke baare me kuch likho"
print("Creative (temp=1.2):", creative_llm.invoke(q).content)
print("Factual (temp=0):", factual_llm.invoke(q).content)


# ============================================
# TRY IT YOURSELF:
# 1. model="gpt-4o-mini" ko "gpt-4o" me badal kar dekho farak (cost zyada hoga, dhyan rakho).
# 2. Same question ko factual_llm se 2 baar invoke karo - kya answer same aata hai?
#    Phir creative_llm se 2 baar - answer alag aata hai? Kyun?
# 3. .invoke() ki jagah llm.stream("...") try karo aur loop se print karo
#    (ye dekhne ke liye ki streaming kaise kaam karta hai)
# ============================================
