"""
TOPIC: PromptTemplate - dynamic prompt banana

CONCEPT:
Hardcoded string ki jagah placeholders ({variable}) use karte ho,
taaki same template ko different values ke saath reuse kar sako.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# --- Simple template, ek variable ---
prompt1 = ChatPromptTemplate.from_template(
    "Tum ek {role} ho. User ka sawal: {question}"
)

chain1 = prompt1 | llm | parser
result = chain1.invoke({"role": "Hindi tutor", "question": "Verb kya hota hai?"})
print("Simple template output:\n", result)


# --- System + Human messages alag se (better control persona ke liye) ---
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Tum ek strict {subject} teacher ho. Hamesha Hinglish me jawab do."),
    ("human", "{question}")
])

chain2 = prompt2 | llm | parser
result2 = chain2.invoke({"subject": "Maths", "question": "2x + 5 = 15, x kya hoga?"})
print("\nSystem+Human template output:\n", result2)


# --- Same template, multiple alag-alag inputs ke saath reuse ---
print("\n--- Same template, 3 alag questions ---")
questions = ["Noun kya hota hai?", "Adjective kya hota hai?", "Pronoun kya hota hai?"]
for q in questions:
    ans = chain1.invoke({"role": "Hindi tutor", "question": q})
    print(f"Q: {q}\nA: {ans}\n")


# ============================================
# TRY IT YOURSELF:
# 1. Apna ek template banao 3 variables ke saath (e.g. role, tone, question).
# 2. ek "system" message likho jisme tum LLM ko bolo ki "hamesha JSON format me jawab do"
#    aur dekho actually LLM kaisa response deta hai.
# 3. prompt1.invoke({...}) ko bina llm ke call karo (sirf prompt object pe)
#    aur print karo - dekho ye kya return karta hai (formatted prompt object).
# ============================================
