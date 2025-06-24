# import streamlit as st
# import os
# import sys
# from typing import Literal

# # Setup import paths
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from agents.graph_builder import app

# st.set_page_config(
#     page_title="Post-Discharge Medical AI Assistant",
#     page_icon="🏥",
#     layout="centered"
# )

# # Initialize session state for chat history as a list of message dicts
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []  # Each item: {"role": "user"|"assistant", "content": str}
# if "patient_verified" not in st.session_state:
#     st.session_state.patient_verified = False
# if "current_patient" not in st.session_state:
#     st.session_state.current_patient = None

# st.title("🏥 Post-Discharge Medical AI Assistant")
# st.markdown("---")

# def create_agent_response(response: str, agent_type: Literal["receptionist", "clinical"]) -> str:
#     icon = "👩‍⚕️" if agent_type == "receptionist" else "👨‍⚕️"
#     agent_name = "Receptionist" if agent_type == "receptionist" else "Clinical Specialist"
#     return f"{icon} **{agent_name}:** {response}"

# # Patient Verification Form
# if not st.session_state.patient_verified:
#     with st.form("patient_verification"):
#         # st.subheader("🔒 Patient Verification")
#         # patient_id = st.text_input("Enter Patient ID", placeholder="e.g., P001")
#         # patient_name = st.text_input("Enter Patient Name (Case-Sensitive)", placeholder="e.g., John Smith")
#         # verify_submitted = st.form_submit_button("Verify Identity")
#         # if verify_submitted:
#         #     if patient_id and patient_name:
#         #         # Initial verification through receptionist agent
#         #         initial_state = {
#         #             "patient_id": patient_id.strip(),
#         #             "patient_name": patient_name.strip(),
#         #             "query": "Verify my identity"
#         #         }
#                 try:
#                     result = app.invoke(initial_state)
#                     if "verified" in result and result["verified"]:
#                         st.session_state.patient_verified = True
#                         st.session_state.current_patient = {
#                             "id": patient_id,
#                             "name": patient_name
#                         }
#                         st.rerun()
#                     else:
#                         st.error("❌ Patient verification failed. Please check your ID and name.")
#                 except Exception as e:
#                     st.error(f"❌ Error during verification: {str(e)}")
#             # else:
#             #     st.warning("⚠️ Please enter both Patient ID and Name.")

# # Main Chat Interface (Only shown after verification)
# if st.session_state.patient_verified:
#     st.success(f"✅ Identity Verified - Welcome, {st.session_state.current_patient['name']}!")
    
#     # Chat input at the bottom
#     with st.form("chat_input", clear_on_submit=True):
#         user_query = st.text_area(
#             "Type your message...",
#             placeholder="Ask about your medications, symptoms, or discharge instructions...",
#             height=80
#         )
#         submitted = st.form_submit_button("Send")
        
#         if submitted and user_query:
#             # Add user message to chat history
#             st.session_state.chat_history.append({"role": "user", "content": user_query.strip()})
#             try:
#                 # Pass the full chat history to the agent graph
#                 config = {"configurable": {"thread_id": "1"}}
#                 response = app.invoke({"messages": st.session_state.chat_history}, config)
#                 # Extract agent response
#                 agent_msg = response["messages"][-1]["content"] if response.get("messages") else "[No response]"
#                 # Determine agent type (optional: you can add logic to detect clinical handoff)
#                 agent_type = "clinical" if "clinical" in agent_msg.lower() else "receptionist"
#                 st.session_state.chat_history.append({"role": "assistant", "content": create_agent_response(agent_msg, agent_type)})
#                 st.rerun()
#             except Exception as e:
#                 st.session_state.chat_history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
#                 st.rerun()

#     # Display Chat History (oldest at top)
#     st.markdown("### 💬 Conversation History")
#     for msg in st.session_state.chat_history:
#         if msg["role"] == "user":
#             st.markdown(f"🧑 **You:** {msg['content']}")
#         else:
#             st.markdown(msg["content"])
    
#     # Reset Button
#     if st.button("🔄 Start New Session"):
#         st.session_state.patient_verified = False
#         st.session_state.chat_history = []
#         st.session_state.current_patient = None
#         st.rerun()

# st.markdown("---")
# st.markdown("*This is an AI assistant. For medical emergencies, please contact your healthcare provider directly.*")




import streamlit as st
import os
import sys
from typing import Literal

# Setup import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.graph_builder import app  # LangGraph Swarm compiled with receptionist + clinical agent

# --------------------------- Streamlit Config --------------------------- #
st.set_page_config(
    page_title="Post-Discharge Medical AI Assistant",
    page_icon="🏥",
    layout="centered"
)
# st.markdown("""
#     <style>
#     .chat-history {
#         max-height: 400px;
#         overflow-y: auto;
#         padding: 1rem;
#         border: 1px solid #ddd;
#         border-radius: 10px;
#         background-color: #f9f9f9;
#     }
#     </style>
# """, unsafe_allow_html=True)


# --------------------------- Session State --------------------------- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Each: {"role": "user"|"assistant", "content": str}

# --------------------------- Utility Function --------------------------- #
def create_agent_response(response: str, agent_type: Literal["receptionist", "clinical"]) -> str:
    icon = "👩‍⚕️" if agent_type == "receptionist" else "👨‍⚕️"
    agent_name = "Receptionist" if agent_type == "receptionist" else "Clinical Specialist"
    print(f"Agent Type: {agent_type}, Response: {response}")
    return f"{icon} **{agent_name}:** {response}"

# --------------------------- Title --------------------------- #
st.title("🏥 Post-Discharge Medical AI Assistant")
st.markdown("Feel free to ask about your discharge report, follow-up care, or any post-discharge instructions.")
st.markdown("---")


# --------------------------- Chat History --------------------------- #
st.markdown("### 💬 Conversation History")
chat_container = st.container()

with chat_container:
    st.markdown(
        '''<div class="chat-history" style="max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">''',
        unsafe_allow_html=True
    )
    st.markdown("**System: Please Enter Patient Id:**")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑 **You:** {msg['content']}")
        else:
            st.markdown(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------- Chat Input Form (Fixed at Bottom) --------------------------- #
st.markdown("<div style='height: 2rem '></div>", unsafe_allow_html=True)  # Spacer
with st.form("chat_input", clear_on_submit=True):
    user_query = st.text_area(
        "Type your message...",
        placeholder="Hi! I have a question about my discharge report...",
        height=80
    )
    submitted = st.form_submit_button("Send")

    if submitted and user_query:
        # Save user message
        st.session_state.chat_history.append({"role": "user", "content": user_query.strip()})
        try:
            config = {"configurable": {"thread_id": "1"}}
            response = app.invoke({"messages": st.session_state.chat_history}, config=config)
            agent_msg = "[No response]"
            if response.get("messages"):
                last_message = response["messages"][-1]
                agent_msg = last_message.content
            agent_type = "clinical" if "clinical" in agent_msg.lower() else "receptionist"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": create_agent_response(agent_msg, agent_type)
            })
            st.rerun()
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })
            st.rerun()

# --------------------------- Reset Button --------------------------- #
if st.button("🔄 Start New Session"):
    st.session_state.chat_history = []
    st.rerun()

# --------------------------- Footer --------------------------- #
st.markdown("---")
st.markdown("*This assistant is for informational purposes only. For medical emergencies, contact your healthcare provider directly.*")
