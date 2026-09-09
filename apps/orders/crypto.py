from cryptography.fernet import Fernet
from django.conf import settings

_fernet = Fernet(settings.PHONE_ENCRYPTION_KEY)

def encrypt_phone(phone: str) -> str:
    return _fernet.encrypt(phone.encode()).decode()

def decrypt_phone(token: str) -> str:
    return _fernet.decrypt(token.encode()).decode()