# LangChain Practice (VS Code + OpenAI)

Ye folder me 8 chhote Python files hain — har ek ek topic practice karne ke liye.
Order se (00 → 07) karna, kyunki concepts upar wale se aage build hote hain.

## Setup (ek baar karna hai)

1. **VS Code me ye folder open karo** (File → Open Folder)

2. **Virtual environment banao** (terminal me, VS Code ke andar hi `Ctrl + ~` se terminal kholo):
   ```
   python -m venv venv
   ```

3. **Activate karo:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

   (Activate hone par terminal me `(venv)` dikhna chahiye)

4. **Packages install karo:**
   ```
   pip install -r requirements.txt
   ```

5. **API key set karo:**
   - `.env.example` file ko copy karke naam `.env` rakho
   - Usme apni API keys paste karo: 
     `OPENAI_API_KEY=sk-...`
     `NVIDIA_API_KEY=nvapi-...`
   - Key yahan se milegi: https://platform.openai.com/api-keys
   - **Important**: `.env` file kabhi GitHub par push mat karna (key leak ho jayegi)

6. **VS Code Python extension** install kar lo (agar nahi hai) — Extensions tab me "Python" search karo (by Microsoft).

## Run kaise karein

Har file independent run hoti hai:
```
python 00_understanding_runnable_classes.py
python 01_llm_basics.py
python 02_prompt_template.py
...
```

Ya VS Code me file khol kar upar-right "Run Python File" button (▶️) dabao.

## File order aur topic

| File | Topic |
|---|---|
| `00_understanding_runnable_classes.py` | Classes/OOP — sab LangChain objects "Runnable" kyun hote hain |
| `01_llm_basics.py` | LLM wrapper — model ko call karna |
| `02_prompt_template.py` | PromptTemplate — dynamic prompts banana |
| `03_simple_sequential_chain.py` | SimpleSequentialChain (SSC) |
| `04_sequential_chain.py` | SequentialChain (SC) — multiple named outputs |
| `05_lcel_basics.py` | LCEL — modern pipe (`|`) style chains |
| `06_memory.py` | Memory — conversation yaad rakhna |
| `07_agents.py` | Agents — LLM khud tool choose kare |
| `08_output_parsers.py` | Output Parsers — raw text ko structured data me convert karna |

Har file ke end me **"TRY IT YOURSELF"** section hai — wahan khud code likh kar practice karo.
