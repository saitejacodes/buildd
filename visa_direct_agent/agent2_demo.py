# agent2_demo.py

import requests
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

AGENT1_API_URL = "http://localhost:8000"
AGENT2_KEY = "VISADIRECT-A1B2C3"

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

AGENT2_SYSTEM_PROMPT = """
You are Agent 2 - an implementation agent.
You receive fast implementation summaries from Agent 1 and use them to write complete, production-ready Python code.

When given a summary, produce:
1. Complete working Python implementation
2. With proper error handling
3. With comments explaining each step
4. Ready to run in production
"""

def agent2_get_knowledge(question: str) -> tuple[str, str]:
    """Step 1: Buy knowledge from Agent 1"""
    try:
        response = requests.post(
            f"{AGENT1_API_URL}/ask-agent1",
            json={
                "key": AGENT2_KEY,
                "question": question
            },
            timeout=30
        )
        data = response.json()
        
        if not data["access"]:
            return None, data["reason"]
        
        return data["answer"], None
        
    except Exception as e:
        return None, str(e)

def agent2_build_implementation(summary: str, task: str) -> str:
    """Step 2: Convert summary to full implementation"""
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": AGENT2_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Task: {task}\n\nFast Summary from Agent 1:\n{summary}\n\nNow write complete production-ready Python implementation."
            }
        ],
        temperature=0.1,
        max_tokens=1500
    )
    
    return response.choices[0].message.content

def run_agent2(task: str):
    """Full Agent 2 pipeline"""
    
    print(f"\nAgent 2 starting task:")
    print(f"   {task}")
    print(f"\nContacting Agent 1 with key: {AGENT2_KEY}")

    # Step 1 - Get knowledge from Agent 1
    summary, error = agent2_get_knowledge(task)

    if error:
        print(f"\nAccess Denied: {error}")
        return

    print(f"\nKnowledge received from Agent 1!")
    print(f"\nFast Summary:\n{summary}")

    # Step 2 - Build full implementation
    print(f"\nAgent 2 building full implementation...")
    
    implementation = agent2_build_implementation(summary, task)

    print(f"\nFinal Implementation:")
    print(implementation)

if __name__ == "__main__":
    run_agent2("Implement a complete fund transfer using Visa Direct API with error handling")
