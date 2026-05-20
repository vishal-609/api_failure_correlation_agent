import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# Set up the connection to the AI provider (Groq)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

def analyze_transaction(item):
    # Extract the basic information from the transaction data we passed in
    cid = item.get("correlationId", "UNKNOWN")
    failures = item.get("failures", [])
    events = item.get("events", [])
    chain = item.get("dependency_chain", "None")

    # Convert the lists of errors and events into readable text blocks for the AI to read
    failure_text = "\n".join([f"{f.get('system', 'Unknown')} - {f.get('eventType', 'Unknown')} - {f.get('details_or_flowName', '')}" for f in failures])
    timeline = "\n".join([f"{e.get('timestamp', 'Unknown')} - {e.get('system', 'Unknown')} - {e.get('eventType', 'Unknown')} - {e.get('details_or_flowName', '')}" for e in events])

    # This is the exact instruction manual and data we are sending to the AI
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
        # Send the prompt to the AI and wait for its response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer that follows structural algorithms without deviation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0 # Temperature 0.0 means the AI will be strictly factual and not "creative" or random
        )
        
        # Grab the actual text the AI sent back
        raw_text = response.choices[0].message.content
        
        # Remove the <thinking> block from the AI's response so your final report looks clean and professional
        if "</thinking>" in raw_text:
            final_text = raw_text.split("</thinking>")[-1].strip()
        else:
            final_text = raw_text

        # Remove any leftover formatting symbols (like bolding or code blocks) and return the final text
        return final_text.replace("*", "").replace("#", "").replace("`", "").strip()
        
    except Exception as e:
        return f"Error: {str(e)}"