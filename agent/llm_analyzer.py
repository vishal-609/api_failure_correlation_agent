import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

def analyze_transaction(item):
    cid = item.get("correlationId", "UNKNOWN")
    failures = item.get("failures", [])
    events = item.get("events", [])
    chain = item.get("dependency_chain", "None")

    if not failures:
        return f"{cid} -> NO_FAILURE"

    failure_text = "\n".join([f"{f.get('system', 'Unknown')} - {f.get('eventType', 'Unknown')} - {f.get('details', '')}" for f in failures])
    timeline = "\n".join([f"{e.get('timestamp', 'Unknown')} - {e.get('system', 'Unknown')} - {e.get('eventType', 'Unknown')} - {e.get('details', '')}" for e in events])

    prompt = f"""You are an expert Site Reliability Engineer.

Dependency Chain:
{chain}

Failure Events:
{failure_text}

Timeline:
{timeline}

Instructions:
You must determine the Root Cause strictly by isolating the deepest failing system in the Dependency Chain. 
Follow this exact step-by-step algorithm:
Step 1: Identify the VERY LAST system at the end of the Dependency Chain.
Step 2: Check if that specific system appears in the "Failure Events" list with an ERROR.
Step 3: If YES, that system is your Root Cause. You are done.
Step 4: If NO, move one step backwards up the Dependency Chain to the previous system and repeat Step 2.

Explain the reason briefly by stating the algorithm's result.
Suggest practical fixes.

STRICT OUTPUT FORMAT:
Root Cause: [System Name]

Reason: [Short explanation]

Fix:
Step 1: [Action]
Step 2: [Action]
Step 3: [Action]

IMPORTANT:
Plain text only.
No markdown.
No symbols like asterisks, hash marks, backticks, or dashes.
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer."},
                {"role": "user", "content": prompt}
            ]
        )
        
        text = response.choices[0].message.content
        return text.replace("*", "").replace("#", "").replace("`", "").strip()
        
    except Exception as e:
        return f"Error: {str(e)}"