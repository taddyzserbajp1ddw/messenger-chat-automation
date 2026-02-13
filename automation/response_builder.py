RESPONSES = {
    "welcome": "Hello! How can I help you today?",
    "help": "Send 'status' to check the system, or describe your request.",
    "status": "System status: OK.",
    "fallback": "Sorry, I didn't understand that. Type 'help' for options."
}

def build_response(key: str) -> str:
    return RESPONSES.get(key, RESPONSES["fallback"])
