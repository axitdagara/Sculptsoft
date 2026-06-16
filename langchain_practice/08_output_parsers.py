"""
TOPIC: Output Parsers - LLM ke raw text ko structured data me convert karna

CONCEPT:
LLM hamesha TEXT return karta hai. Agar tumhe wo text Python me
istemaal karna hai (jaise list, dictionary, ya specific object),
to Output Parser us text ko structured format me convert karta hai.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- 1. StrOutputParser - sabse simple, sirf text nikalta hai ---
prompt1 = ChatPromptTemplate.from_template("Ek line me bata: {topic}")
chain1 = prompt1 | llm | StrOutputParser()
print("StrOutputParser output (plain string):")
print(chain1.invoke({"topic": "AI"}), "\n")


# --- 2. JsonOutputParser - LLM ko JSON format me jawab dene ko bolta hai ---
prompt2 = ChatPromptTemplate.from_template(
    "Is movie ke baare me JSON format me batao with keys: "
    "title, year, genre. Movie: {movie}"
)
chain2 = prompt2 | llm | JsonOutputParser()
result2 = chain2.invoke({"movie": "Inception"})
print("JsonOutputParser output (Python dict):")
print(result2)
print("Type:", type(result2))
print("Sirf genre:", result2["genre"], "\n")


# --- 3. PydanticOutputParser - strict schema/class define karke parse karo ---
# Pydantic BaseModel ek "class" hai jo data ka exact structure define karti hai

class MovieInfo(BaseModel):
    title: str = Field(description="Movie ka naam")
    year: int = Field(description="Release year")
    genre: str = Field(description="Movie ka genre")
    rating_out_of_10: float = Field(description="Tumhara estimated rating")

# with_structured_output() - modern, clean tareeka schema follow karwane ka
structured_llm = llm.with_structured_output(MovieInfo)

prompt3 = ChatPromptTemplate.from_template("Is movie ke baare me batao: {movie}")
chain3 = prompt3 | structured_llm

result3 = chain3.invoke({"movie": "Interstellar"})
print("Structured output (Pydantic object):")
print(result3)
print("Type:", type(result3))
print("Sirf rating:", result3.rating_out_of_10)


# ============================================
# TRY IT YOURSELF:
# 1. MovieInfo class me ek naya field add karo: "director: str"
#    aur dekho LLM use bhi fill kar deta hai bina extra instruction ke.
# 2. Ek naya Pydantic class banao "RecipeInfo" with fields:
#    name, ingredients (list[str]), cooking_time_minutes (int)
#    aur usse ek recipe generate karwao structured format me.
# 3. result3.model_dump() try karo - ye Pydantic object ko dictionary me convert karta hai.
# ============================================
