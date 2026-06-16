"""
TOPIC: Memory - conversation yaad rakhna

CONCEPT:
LLM by default STATELESS hai - har call independent hota hai.
Memory classes pichle messages ko store karke next call ke prompt
me automatically inject kar dete hain.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

# --- PEHLE DEKHO: memory ke BINA kya hota hai ---
print("=== Memory ke BINA ===")
print("Call 1:", llm.invoke("Mera naam Rahul hai").content)
print("Call 2:", llm.invoke("Mera naam kya hai?").content)
# Call 2 me LLM ko nahi pata hoga - har invoke() independent hai


# --- AB memory ke SAATH ---
print("\n=== Memory ke SAATH ===")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Tum ek helpful assistant ho."),
    ("placeholder", "{history}"),   # yahan pichle messages inject honge
    ("human", "{input}")
])
chain = prompt | llm | StrOutputParser()

# Har session ki history store karne ke liye ek simple dictionary
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user-1"}}

print("Call 1:", chain_with_memory.invoke({"input": "Mera naam Rahul hai"}, config=config))
print("Call 2:", chain_with_memory.invoke({"input": "Mera naam kya hai?"}, config=config))
# Ab Call 2 me "Rahul" yaad rahega, kyunki same session_id use hua


# --- Dusra session bilkul fresh hota hai ---
config2 = {"configurable": {"session_id": "user-2"}}
print("\nNaya session (user-2):", chain_with_memory.invoke({"input": "Mera naam kya hai?"}, config=config2))
# Yahan LLM ko nahi pata hoga - kyunki ye alag session hai, alag history hai


# ============================================
# TRY IT YOURSELF:
# 1. user-1 session me 3-4 messages bhejo (alag-alag facts batao apne baare me),
#    phir poocho "mere baare me jo bataya wo sab repeat karo" - dekho kitna yaad rakhta hai.
# 2. print(store["user-1"].messages) karke dekho ki andar kya stored hai.
# 3. Socho: agar conversation bahut LAMBI ho jaye (100+ messages), to har baar
#    pura history bhejna costly hoga (tokens). Internet par search karo
#    "ConversationSummaryMemory" ke baare me - ye is problem ko kaise solve karta hai?
# ============================================
