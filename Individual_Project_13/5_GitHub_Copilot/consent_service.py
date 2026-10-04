from copy import deepcopy
from datetime import datetime
from uuid import uuid4


_consents = {}
_audit_log = []


def _validate_time_pair(start_time, expiry_time):
    if not isinstance(start_time, datetime) or not isinstance(expiry_time, datetime):
        raise TypeError("start_time and expiry_time must be datetime objects")

    start_is_aware = start_time.utcoffset() is not None
    expiry_is_aware = expiry_time.utcoffset() is not None
    if start_is_aware != expiry_is_aware:
        raise ValueError("start_time and expiry_time must both be timezone-aware or naive")


def _current_time(reference_time):
    return datetime.now(tz=reference_time.tzinfo)


def grant_consent(patient_id, doctor_id, record_id, expiry_time, doctor_verified):
    """Grant a verified doctor access to one patient's health record until expiry."""
    for name, value in (
        ("patient_id", patient_id),
        ("doctor_id", doctor_id),
        ("record_id", record_id),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")

    if doctor_verified is not True:
        raise PermissionError("Consent can only be granted to a verified clinic doctor")
    if not isinstance(expiry_time, datetime):
        raise TypeError("expiry_time must be a datetime object")

    start_time = _current_time(expiry_time)
    if expiry_time <= start_time:
        raise ValueError("expiry_time must be in the future")

    consent_id = uuid4().hex
    consent = {
        "consent_id": consent_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "record_id": record_id,
        "start_time": start_time,
        "expiry_time": expiry_time,
        "revoked_at": None,
    }
    _consents[consent_id] = consent
    _audit_log.append(
        {
            "event": "grant",
            "consent_id": consent_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "record_id": record_id,
            "timestamp": start_time,
        }
    )
    return deepcopy(consent)


def revoke_consent(consent_id):
    """Revoke an existing consent that has not yet expired."""
    consent = _consents.get(consent_id)
    if consent is None:
        raise KeyError(f"No consent found for id {consent_id!r}")
    if consent["revoked_at"] is not None:
        raise ValueError("Consent has already been revoked")

    revoked_at = _current_time(consent["expiry_time"])
    if revoked_at >= consent["expiry_time"]:
        raise ValueError("Expired consent cannot be revoked")

    consent["revoked_at"] = revoked_at
    _audit_log.append(
        {
            "event": "revoke",
            "consent_id": consent_id,
            "patient_id": consent["patient_id"],
            "doctor_id": consent["doctor_id"],
            "record_id": consent["record_id"],
            "timestamp": revoked_at,
        }
    )
    return deepcopy(consent)


def is_consent_valid(consent_id_or_start_time, expiry_time=None):
    """Check a stored consent by ID, or a time window using the legacy API."""
    if expiry_time is None:
        consent = _consents.get(consent_id_or_start_time)
        if consent is None:
            return False
        if consent["revoked_at"] is not None:
            return False
        start_time = consent["start_time"]
        expiry_time = consent["expiry_time"]
    else:
        start_time = consent_id_or_start_time

    _validate_time_pair(start_time, expiry_time)
    current_time = _current_time(expiry_time)
    return start_time <= current_time < expiry_time


def get_audit_log():
    """Return a snapshot of the append-only grant/revoke event log."""
    return tuple(deepcopy(_audit_log))
