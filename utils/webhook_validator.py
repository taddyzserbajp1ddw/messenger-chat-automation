def verify_webhook(mode: str, token: str, challenge: str, expected_token: str):
    if mode == "subscribe" and token == expected_token:
        return challenge
    return None
