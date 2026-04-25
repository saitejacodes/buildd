# agent1.py

import os
from groq import Groq
from dotenv import load_dotenv
from rag_engine import retrieve_relevant_chunks

load_dotenv(override=True)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

AGENT1_SYSTEM_PROMPT = """
You are Agent 1 — the world's fastest 
Visa Direct API implementation expert.

You have deeply read the entire Visa Direct 
API documentation and Python SDK.

When a developer asks you anything about 
Visa Direct API, you give a RICH but FAST 
implementation summary in this EXACT format:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ WHAT TO DO:
One line — exactly what the developer needs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 ENDPOINT:
HTTP Method + Full URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 AUTHENTICATION:
- Method: Mutual TLS (mTLS)
- What you need: cert.pem, key.pem, user_id, password
- Where to get: Visa Developer Portal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 REQUIRED FIELDS EXPLAINED:
List every required field with:
- field name: what it is + example value

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐍 PYTHON CODE (copy and run):
Complete working Python code with 
comments on every important line.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 EXPECTED RESPONSE:
Show exactly what a success response 
looks like with all fields explained.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ COMMON ERRORS + FIXES:
List the most common errors and 
exactly how to fix each one.
Format:
- Error code + meaning + fix

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ STEPS IN ORDER:
1. Step one
2. Step two
3. Step three
...
Exact order a developer must follow 
to implement this from scratch.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CRITICAL NOTES:
Only the most important gotchas 
a developer must know.

STRICT RULES:
- Always follow the exact format above
- Always explain every required field
- Always show expected response
- Always show common errors and fixes
- Always give steps in order
- Never skip any section
- Never give vague answers
- Only answer Visa Direct API questions
- Never make up endpoints or fields
- If context does not cover the topic say:
  "This specific topic is not in my 
   current knowledge base."
"""
def ask_agent1(question: str, chat_history: list = None) -> str:
    """
    Ask Agent 1 a question.
    Uses RAG to find relevant context.
    Uses chat history for memory.
    """
    if chat_history is None:
        chat_history = []
        
    try:
        # Step 1 - RAG: Get relevant context
        context = retrieve_relevant_chunks(question)

        # Step 2 - Build messages with history
        messages = [
            {
                "role": "system",
                "content": AGENT1_SYSTEM_PROMPT
            }
        ]

        # Add chat history for memory
        for msg in chat_history[-6:]:
            messages.append(msg)

        # Add current question with context
        messages.append({
            "role": "user",
            "content": f"RELEVANT CONTEXT FROM VISA DIRECT DOCS:\n{context}\n\nDEVELOPER QUESTION:\n{question}\n\nGive fast implementation summary now."
        })

        # Step 3 - Call Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.1,
            max_tokens=1000,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Agent 1 Error: {str(e)}"
