import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_order_token(encrypted_phone: str) -> str:
    payload = {
        "ep": encrypted_phone,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=6),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")