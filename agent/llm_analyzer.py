import os
from dotenv import load_dotenv
from openai import OpenAI
from config import COLUMN_CORRELATION_ID, COLUMN_SYSTEM, COLUMN_EVENT_TYPE, COLUMN_DETAILS, COLUMN_TIMESTAMP

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

def analyze_transaction(item):
    cid = item.get(COLUMN_CORRELATION_ID, "UNKNOWN")
    failures = item.get("failures", [])
    events = item.get("events", [])
    chain = item.get("dependency_chain", "None")

    failure_text = "\n".join([f"{f.get(COLUMN_SYSTEM, 'Unknown')} - {f.get(COLUMN_EVENT_TYPE, 'Unknown')} - {f.get(COLUMN_DETAILS, '')}" for f in failures])
    timeline = "\n".join([f"{e.get(COLUMN_TIMESTAMP, 'Unknown')} - {e.get(COLUMN_SYSTEM, 'Unknown')} - {e.get(COLUMN_EVENT_TYPE, 'Unknown')} - {e.get(COLUMN_DETAILS, '')}" for e in events])

    prompt = f"""You are an expert Site Reliability Engineer.

Dependency Chain:
{chain}

Failure Events:
{failure_text}

Timeline:
{timeline}

Instructions:
You must determine the Root Cause strictly by isolating the deepest failing system in the Dependency Chain. 

Before generating the final output, think step-by-step internally inside a <thinking> block following this exact algorithm:
1. Identify the VERY LAST system at the end of the Dependency Chain.
2. Check if that specific system appears in the "Failure Events" list with an ERROR.
3. If YES, that system is your Root Cause. Stop.
4. If NO, move exactly one step backwards up the Dependency Chain to the previous system and repeat the check.

STRICT OUTPUT FORMAT:
<thinking>
[Write your step-by-step verification process here following the algorithm precisely]
</thinking>

Root Cause: [System Name]

Reason: [Short explanation]

Fix:
Step 1: [Action]
Step 2: [Action]
Step 3: [Action]

IMPORTANT:
Plain text only for the final sections.
No markdown or symbols like asterisks, hash marks, backticks, or dashes in the final output.
"""

    try:
        response = client.chat.completions.create(
            # UPDATED: Using the newest supported 70B model
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer that follows structural algorithms without deviation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0 # Force deterministic, zero-hallucination execution
        )
        
        raw_text = response.choices[0].message.content
        
        # Strip out the thinking block so your final email and file stay perfectly clean
        if "</thinking>" in raw_text:
            final_text = raw_text.split("</thinking>")[-1].strip()
        else:
            final_text = raw_text

        return final_text.replace("*", "").replace("#", "").replace("`", "").strip()
        
    except Exception as e:
        return f"Error: {str(e)}"