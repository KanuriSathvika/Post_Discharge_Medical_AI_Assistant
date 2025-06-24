# from langgraph import tool
from langchain_core.messages import AIMessage, HumanMessage


from backend.mongo_database import get_patient_by_name

def patient_report_tool(patient_name:str) -> dict:
    """
    Tool to fetch patient details and respond to queries.
    This tool retrieves patient information based on the provided patient ID
    Args:
        patient_id (str): Unique identifier for the patient.
        patient_name (str): Name of the patient.
        query (str): The query or request from the patient.
    
    Returns:
        str: Response containing patient details or query answer.
    """
    # Placeholder for actual implementation
    #get patient details from database
    patient = get_patient_by_name(patient_name)
    if not patient:
        return "❌ No patient found with name: {patient_id}."
    # return patient details if name matches
    # if patient_name != patient["patient_name"]:     
    #     return f"❌ Name mismatch. Entered: {patient_name}, Expected: {patient['patient_name']}"
    # return patient summary   
    # 
    if patient_name== patient["patient_name"]:
        return f"✅ Patient found: {patient['patient_name']}. Please enter Patiend Id to confirm."  
    summary = (
        f"Hello {patient['patient_name']}, here is your discharge summary:\n"
        f"Diagnosis: {patient['primary_diagnosis']}\n"
        f"Medications: {', '.join(patient['medications'])}\n"
        f"Dietary Restrictions: {patient['dietary_restrictions']}\n"
        f"Follow-up: {patient.get('follow_up', 'N/A')}"
    )
    return patient