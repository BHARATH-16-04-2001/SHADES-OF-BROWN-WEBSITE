import hashlib

def channel_group_for(encrypted_phone: str) -> str:
    digest = hashlib.sha256(encrypted_phone.encode()).hexdigest()
    return f"orders_{digest[:40]}"


# def channel_group_for(encrypted_phone: str) -> str:
#     # Channels group names must match ^[a-zA-Z0-9\-_.]{1,100}$ — Fernet's
#     # base64 padding ('=') violates that, so we strip it. Otherwise this
#     # is exactly the encryptedPhoneNumber value your customer socket
#     # authenticates with.
#     return encrypted_phone.rstrip("=")