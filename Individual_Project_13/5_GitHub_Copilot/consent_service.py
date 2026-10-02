from datetime import datetime


def is_consent_valid(start_time, expiry_time):
    """
    Check if the consent is still valid based on the current time.

    Args:
        start_time (datetime): The start time of the consent.
        expiry_time (datetime): The expiry time of the consent.
        
    Returns:
        bool: True if the consent is valid, False otherwise.
    """
    current_time = datetime.now()
    return start_time <= current_time <= expiry_time

def grant_consent(patient_id, doctor_id, record_id, expiry_time):
    """
    Grant consent for a doctor to access a patient's medical record.

    Args:
        patient_id (str): The ID of the patient.
        doctor_id (str): The ID of the doctor.
        record_id (str): The ID of the medical record.
        expiry_time (datetime): The time when the consent expires.
    Returns:
        dict: A dictionary containing the consent details.
    """
    start_time = datetime.now()
    consent_details = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "record_id": record_id,
        "start_time": start_time,
        "expiry_time": expiry_time
    }
    return consent_details