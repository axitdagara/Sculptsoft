"""
TOPIC: SimpleSequentialChain (SSC) - legacy chain, single input -> single output

CONCEPT:
Har step ka EK output hi next step ka EK input banta hai. Sirf last
output milta hai, beech ke outputs track nahi hote.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

# Step 1: topic -> joke
joke_prompt = PromptTemplate.from_template(
    "Is topic par ek chhota joke banao: {topic}"
)
joke_chain = LLMChain(llm=llm, prompt=joke_prompt)

# Step 2: joke -> uska explanation (ki joke funny kyun hai)
explain_prompt = PromptTemplate.from_template(
    "Ye joke ka explanation do ki ye funny kyun hai: {joke}"
    # NOTE: yahan variable name "joke" hai - SSC me variable ka naam matter
    # nahi karta, kyunki ye sirf agle step ka SOLE input bnta hai
)
explain_chain = LLMChain(llm=llm, prompt=explain_prompt)

# Dono chains ko jodo
overall_chain = SimpleSequentialChain(
    chains=[joke_chain, explain_chain],
    verbose=True  # True rakhne se beech ke steps terminal me dikhenge
)

result = overall_chain.invoke({"input": "Programmers"})
print("\n=== FINAL OUTPUT (sirf last step ka) ===")
print(result["output"] if isinstance(result, dict) else result)

# NOTICE: humein joke nahi mila yahan, sirf explanation mila -
# SSC sirf LAST output return karta hai


# ============================================
# TRY IT YOURSELF:
# 1. Ek teesra chain add karo: explanation -> "ye 1-5 rating do funniness ki"
#    aur overall_chain me 3 chains pass karo.
# 2. verbose=False kar ke run karo aur dekho farak (intermediate steps nahi dikhenge).
# 3. Socho: agar tumhe joke AUR explanation dono chahiye final result me,
#    SSC se possible hai kya? (Answer: nahi - isiliye SequentialChain banaya gaya,
#    next file me dekhenge)
# ============================================
