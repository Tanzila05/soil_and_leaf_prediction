from typing import Optional

from db_config import get_disease_collection


def get_disease_info(disease_name: str) -> Optional[dict]:
    """Fetch precautions and medicines for a disease by name."""
    doc = get_disease_collection().find_one(
        {"disease_name": disease_name},
        {"_id": 0, "precautions": 1, "medicines": 1},
    )
    return doc


def parse_medicines(medicines: str) -> list[str]:
    if not medicines:
        return ["No medicine info found in database."]
    return [med.strip() for med in medicines.split(",") if med.strip()]
