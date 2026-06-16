"""
TOPIC: Agents - LLM khud decide karta hai konsa tool use karna hai

CONCEPT:
Chain me steps FIXED hote hain (tumne pehle se order decide kiya).
Agent me LLM khud "sochta" hai ki query ko solve karne ke liye
kaunsa tool chahiye, use call karta hai, result dekhta hai, aur
phir final answer banata hai. Ye ek LOOP hai (ReAct pattern).
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain import hub

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Custom tools banao (@tool decorator se) ---
# Ye normal Python functions hain, LangChain inhe "tool" me convert kar deta hai

@tool
def get_word_length(word: str) -> int:
    """Diye gaye word ki length (number of characters) return karta hai."""
    return len(word)

@tool
def reverse_word(word: str) -> str:
    """Diye gaye word ko reverse (ulta) karke return karta hai."""
    return word[::-1]

@tool
def calculate(expression: str) -> str:
    """Ek simple math expression (jaise '2 + 2 * 3') ko evaluate karta hai."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [get_word_length, reverse_word, calculate]

# --- ReAct prompt template (LangChain hub se ready-made prompt) ---
# Ye prompt LLM ko sikhata hai ki "Thought -> Action -> Observation" pattern follow kare
try:
    prompt = hub.pull("hwchase17/react")
except Exception:
    # Agar hub access na ho to manual ReAct prompt
    prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

result = executor.invoke({
    "input": "'programming' word ki length kya hai, aur use reverse karke bhi batao"
})
print("\n=== FINAL ANSWER ===")
print(result["output"])


print("\n\n--- Doosra example (math tool use karega) ---")
result2 = executor.invoke({"input": "(15 + 7) * 3 kya hota hai?"})
print("\n=== FINAL ANSWER ===")
print(result2["output"])


# ============================================
# TRY IT YOURSELF:
# 1. verbose=True ki output dhyan se padho - dekho LLM "Thought", "Action",
#    "Observation" kaise likh raha hai har step me. Yahi agent ka "soch" hai.
# 2. Apna ek naya tool banao: @tool def count_vowels(word: str) -> int
#    jo word me vowels (a,e,i,o,u) count kare. tools list me add karo.
# 3. Ek aisa question poocho jisme agent ko 2 tools use karne pade ek ke baad ek
#    (jaise "calculate karo 5*5, phir uska result reverse karke string banao")
# ============================================
