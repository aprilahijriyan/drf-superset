from datetime import datetime, timedelta
from typing import Tuple

from cryptography.fernet import Fernet

from .exceptions import TokenExpiredException


def encrypt(message: bytes, exp: timedelta = None) -> Tuple[bytes, bytes]:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    if exp:
        seconds = (datetime.utcnow().replace(microsecond=0) + exp).timestamp()
        pw = fernet.encrypt_at_time(message, int(seconds))
    else:
        pw = fernet.encrypt(message)
    return key, pw


def decrypt(message: bytes, key: bytes) -> bytes:
    fernet = Fernet(key)
    timestamp = fernet.extract_timestamp(message)
    if timestamp:
        exp = datetime.fromtimestamp(timestamp)
        if exp and datetime.utcnow().replace(microsecond=0) > exp:
            raise TokenExpiredException("token has expired")

    data = fernet.decrypt(message)
    return data
