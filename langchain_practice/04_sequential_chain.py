"""
TOPIC: SequentialChain (SC) - multiple named inputs/outputs

CONCEPT:
Har chain ka output_key naam se store hota hai. Tum decide kar sakte ho
final result me KAUNSE outputs chahiye (sirf last wala nahi, beech ke bhi).
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

# Step 1: topic -> title          (output_key = "title")
title_prompt = PromptTemplate.from_template(
    "Is topic ke liye ek catchy blog title banao: {topic}"
)
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key="title")

# Step 2: title -> outline         (output_key = "outline")
outline_prompt = PromptTemplate.from_template(
    "Is blog title ke liye 4-point outline banao: {title}"
)
outline_chain = LLMChain(llm=llm, prompt=outline_prompt, output_key="outline")

# Step 3: outline -> social caption (output_key = "caption")
caption_prompt = PromptTemplate.from_template(
    "Is outline ko dekh kar ek Twitter caption likho (under 280 chars): {outline}"
)
caption_chain = LLMChain(llm=llm, prompt=caption_prompt, output_key="caption")

# Sabko jodo - dhyan do output_variables me teeno naam diye hain
overall_chain = SequentialChain(
    chains=[title_chain, outline_chain, caption_chain],
    input_variables=["topic"],
    output_variables=["title", "outline", "caption"],
    verbose=True
)

result = overall_chain({"topic": "Machine Learning ke beginners ke liye tips"})

print("\n=== FINAL OUTPUT (sab kuch milta hai) ===")
print("Title:", result["title"])
print("\nOutline:", result["outline"])
print("\nCaption:", result["caption"])


# ============================================
# TRY IT YOURSELF:
# 1. output_variables me se "outline" hata do (sirf ["title", "caption"] rakho)
#    aur dekho result dictionary me "outline" key nahi aayegi.
# 2. Ek 4th chain add karo: caption -> "3 relevant hashtags suggest karo"
#    output_key="hashtags" rakho, aur use bhi output_variables me add karo.
# 3. caption_prompt me {topic} bhi add karo (jaise "{outline}... original topic: {topic}")
#    - kya ye kaam karega bina kuch extra kiye? (Answer: haan, kyunki SequentialChain
#    pura state carry karta hai)
# ============================================
