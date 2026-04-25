# key_system.py

VALID_KEYS = {
    "VISADIRECT-A1B2C3": {
        "owner": "Agent-2",
        "plan": "$10",
        "status": "active"
    },
    "VISADIRECT-X9Y8Z7": {
        "owner": "Agent-3",
        "plan": "$10",
        "status": "active"
    },
    "VISADIRECT-M5N6P7": {
        "owner": "Agent-4",
        "plan": "$10",
        "status": "inactive"
    },
}

def verify_key(key: str) -> dict:
    key = key.strip()
    
    if not key:
        return {
            "access": False,
            "reason": "No key provided. Purchase access for $10."
        }
    if key not in VALID_KEYS:
        return {
            "access": False,
            "reason": "Invalid key. Access Denied. Purchase access for $10."
        }
    if VALID_KEYS[key]["status"] != "active":
        return {
            "access": False,
            "reason": "Key is inactive. Please renew your subscription."
        }
    return {
        "access": True,
        "owner": VALID_KEYS[key]["owner"],
        "plan": VALID_KEYS[key]["plan"]
    }
