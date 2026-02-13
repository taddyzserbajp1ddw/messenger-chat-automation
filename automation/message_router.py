def route_message(text: str) -> str:
    text = (text or "").lower().strip()
    if text in ("hi", "hello", "hey"):
        return "welcome"
    if "help" in text:
        return "help"
    if "status" in text:
        return "status"
    return "fallback"
