# app.py

import streamlit as st
from agent1 import ask_agent1
from key_system import verify_key
from doc_loader import save_knowledge_base
from rag_engine import build_vector_store
import os

# -- Page Config --
st.set_page_config(
    page_title="Visa Direct Agent",
    layout="wide"
)

# -- Initialize on first run --
@st.cache_resource
def initialize():
    """Build knowledge base and vector store on startup"""
    save_knowledge_base()
    build_vector_store()
    return True

initialize()

# -- Session State for Chat Memory --
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# -- Header --
st.title("Visa Direct API Agent")
st.markdown("**Stop reading docs. Ask and get working code instantly.**")
st.divider()

# -- Tabs --
tab1, tab2 = st.tabs([
    "Developer Tool",
    "Agent Access Simulator"
])

# ==========================================
# TAB 1 - DEVELOPER TOOL WITH CHAT MEMORY
# ==========================================
with tab1:
    st.subheader("Ask Agent 1 - Visa Direct Fast Implementation")

    # Quick example buttons
    st.markdown("**Quick Examples:**")
    c1, c2, c3, c4 = st.columns(4)
    
    quick_q = None
    if c1.button("Fund Transfer"):
        quick_q = "How do I initiate a fund transfer?"
    if c2.button("Authentication"):
        quick_q = "How do I authenticate with Visa Direct?"
    if c3.button("Check Status"):
        quick_q = "How do I check transaction status?"
    if c4.button("Reverse Transfer"):
        quick_q = "How do I reverse a fund transfer?"

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask anything about Visa Direct API...")

    if quick_q:
        user_input = quick_q

    if user_input:
        # Show user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get Agent 1 response
        with st.chat_message("assistant"):
            with st.spinner("Agent 1 generating fast implementation..."):
                response = ask_agent1(
                    user_input,
                    st.session_state.chat_history
                )
            st.markdown(response)

        # Update histories
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ==========================================
# TAB 2 - AGENT ACCESS SIMULATOR
# ==========================================
with tab2:
    st.subheader("External Agent Knowledge Access Simulator")
    st.markdown(
        "Simulate an external Agent 2 requesting knowledge from Agent 1. Only valid keys get access."
    )

    with st.expander("Test Keys (for demo)"):
        st.markdown(
            "**Valid:** `VISADIRECT-A1B2C3`\n\n"
            "**Valid:** `VISADIRECT-X9Y8Z7`\n\n"
            "**Inactive:** `VISADIRECT-M5N6P7`\n\n"
            "**Invalid:** anything else"
        )

    agent_key = st.text_input(
        "Agent Key:",
        placeholder="VISADIRECT-XXXXXX"
    )

    agent_question = st.text_area(
        "Question for Agent 1:",
        placeholder="How do I do a fund transfer?",
        height=100
    )

    if st.button("Request Knowledge", type="primary", use_container_width=True):
        if not agent_key.strip():
            st.error("No key provided. This is a paid knowledge agent. Purchase access for $10.")
        else:
            verification = verify_key(agent_key)

            if not verification["access"]:
                st.error(f"Access Denied - {verification['reason']}")
            else:
                st.success(f"Key Verified! Welcome {verification['owner']}")
                if agent_question.strip():
                    with st.spinner("Agent 1 sharing knowledge..."):
                        answer = ask_agent1(agent_question)
                    st.markdown("### Knowledge from Agent 1:")
                    st.markdown(answer)
                else:
                    st.info("Key is valid! Enter a question above.")

# -- Footer --
st.divider()
st.markdown("**Visa Direct Agent 1** - Powered by Groq LLaMA 3 + RAG | Built for the Agent Economy")
