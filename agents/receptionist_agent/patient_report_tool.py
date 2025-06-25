"""
patient_report_tool.py
---------------------
This module provides a tool for fetching patient details from the database and responding to queries about patient reports.
"""

# from langgraph import tool  # Uncomment if using LangGraph tool decorator
from langchain_core.messages import AIMessage, HumanMessage  # For message formatting (if needed)

from backend.mongo_database import get_patient_by_name  # Function to fetch patient from DB
from backend.logger import logger  # Logger for tracking tool usage


def patient_report_tool(patient_name: str, agent_name: str = "ReceptionistAgent") -> dict:
    """
    Tool to fetch patient details and respond to queries.
    Retrieves patient information based on the provided patient name.

    Args:
        patient_name (str): Name of the patient.
        agent_name (str): Name of the agent calling the tool (for logging).

    Returns:
        dict or str: Patient details as a dict if found, or an error message string if not found.
    """
    logger.info(f"[PatientReportTool] Called by: {agent_name} | Patient Name: {patient_name}")
    patient = get_patient_by_name(patient_name)
    if not patient:
        logger.info(f"[PatientReportTool] Responded by: {agent_name} | No patient found: {patient_name}")
        return f"❌ No patient found with name: {patient_name}."
    if patient_name == patient["patient_name"]:
        logger.info(f"[PatientReportTool] Responded by: {agent_name} | Patient found: {patient['patient_name']}")
        return f"✅ Patient found: {patient['patient_name']}. Please enter Patient Id to confirm."
    # Optionally, you can return a summary string here if needed
    summary = (
        f"Hello {patient['patient_name']}, here is your discharge summary:\n"
        f"Diagnosis: {patient['primary_diagnosis']}\n"
        f"Medications: {', '.join(patient['medications'])}\n"
        f"Dietary Restrictions: {patient['dietary_restrictions']}\n"
        f"Follow-up: {patient.get('follow_up', 'N/A')}"
    )
    logger.info(f"[PatientReportTool] Responded by: {agent_name} | Summary sent for: {patient['patient_name']}")
    return patient