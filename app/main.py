import streamlit as st
import os
import sys
from datetime import datetime
from typing import Literal

# ---------------------------------------------------------------------- #
#  Path setup – adjust as needed for your project structure
# ---------------------------------------------------------------------- #
# Add the parent directory to sys.path so that backend and agents modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.logger import logger  # Custom logger for app events
from agents.graph_builder import app   # LangGraph Swarm (receptionist + clinical)

# ---------------------------------------------------------------------- #
#  Streamlit config
# ---------------------------------------------------------------------- #
st.set_page_config(
    page_title="Post-Discharge Medical AI Assistant",  # Title in browser tab
    page_icon="🏥",                                   # Favicon
    layout="wide",                                   # Use full screen width
)

# ---------------------------------------------------------------------- #
#  Session State
# ---------------------------------------------------------------------- #
# Initialize chat history and previous sessions in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []          # Current chat messages
if "previous_sessions" not in st.session_state:
    st.session_state.previous_sessions = []     # List of previous chat sessions

# ---------------------------------------------------------------------- #
#  Helpers
# ---------------------------------------------------------------------- #
def create_agent_response(response: str,
                          agent_type: Literal["receptionist", "clinical"]) -> str:
    """
    Format assistant messages for display in the chat.
    Optionally, you can add an emoji avatar or prefix based on agent_type.
    Args:
        response (str): The message from the agent.
        agent_type (Literal): Either 'receptionist' or 'clinical'.
    Returns:
        str: Formatted message for display.
    """
    # avatar = "👩‍⚕️ Receptionist:" if agent_type == "receptionist" else "🩺 Clinical:"
    return f" {response}"

# ---------------------------------------------------------------------- #
#  Layout
# ---------------------------------------------------------------------- #
# Use three columns: left (instructions), middle (chat), right (session history)
left_col, mid_col, right_col = st.columns([1.5, 4, 1.5])

# ----------------------- LEFT COLUMN ---------------------------------- #
with left_col:
    st.markdown(
        "<div style='font-size:0.9rem;color:#666;padding:.5rem 0;'>"
        "<b>Test patient record:</b><br>"
        "Patient ID: <b>P001</b><br>"
        "Name: <b>John Smith</b>"
        "</div>",
        unsafe_allow_html=True,
    )

# ----------------------- MIDDLE COLUMN (main chat) -------------------- #
with mid_col:
    st.title("🏥 Post-Discharge Medical AI Assistant")
    st.markdown(
        "Ask about your discharge report, follow-up care, or any post-discharge instructions."
    )
    st.markdown("---")

    # ---------------- Chat History box -------------------------------- #
    st.markdown("### 💬 Conversation")
    chat_container = st.container() 
    with chat_container:
        # Show initial system prompt if chat is empty
        if not st.session_state.chat_history:
            st.markdown("**System:** Please enter your Patient ID.")
        # Display all chat messages
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"🧑 **You:** {msg['content']}")
            else:
                st.markdown(msg["content"])
    # Spacer for better layout
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ---------------- Input form -------------------------------------- #
    with st.form("chat_input", clear_on_submit=True):
        user_query = st.text_area(
            "Type your message...",
            placeholder="Hi! I have a question about my discharge report…",
            height=68,
        )
        submitted = st.form_submit_button("Send")

        if submitted and user_query.strip():
            logger.info(f"User query: {user_query}")
            st.session_state.chat_history.append(
                {"role": "user", "content": user_query.strip()}
            )
            try:
                # Call the LangGraph agent with the full chat history
                config = {"configurable": {"thread_id": "1"}}
                response = app.invoke({"messages": st.session_state.chat_history},
                                      config=config)

                agent_msg = "[No response]"
                if response.get("messages"):
                    agent_msg = response["messages"][-1].content

                # Determine agent type for formatting (optional)
                agent_type = (
                    "clinical" if "clinical" in agent_msg.lower() else "receptionist"
                )
                st.session_state.chat_history.append(
                    {"role": "assistant",
                     "content": create_agent_response(agent_msg, agent_type)}
                )
                st.rerun()

            except Exception as e:
                logger.error(f"Error: {e}")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"❌ Error: {e}"}
                )
                st.rerun()

    # ---------------- Session controls -------------------------------- #
    st.markdown("---")
    st.markdown(
        "_This assistant is for informational purposes only. In an emergency, contact your healthcare provider._"
    )

# ----------------------- RIGHT COLUMN (session history) --------------- #
with right_col:
    st.markdown("### Previous Chat Sessions")

    if st.button("🔄 Start New Session"):
        if st.session_state.chat_history:
            # Save current chat with a timestamp for session history
            st.session_state.previous_sessions.append(
                {
                    "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
                    "messages": list(st.session_state.chat_history),
                }
            )
        st.session_state.chat_history = []
        st.rerun()

    if st.session_state.previous_sessions:
        # Show most-recent sessions first
        for idx, session in enumerate(
            reversed(st.session_state.previous_sessions), start=1
        ):
            ts = session["timestamp"]
            # Preview: first user message in the session
            preview = next(
                (m["content"] for m in session["messages"] if m["role"] == "user"),
                "  (no messages)",
            )
            label = (
                f"🕒 Session {idx} – {ts}\n"
                f"🧑 {preview[:50]}{'…' if len(preview) > 50 else ''}"
            )
            # Button to load previous session into chat
            if st.button(label, key=f"load_{idx}"):
                st.session_state.chat_history = list(session["messages"])
                st.rerun()
    else:
        st.markdown("_No previous sessions._")
