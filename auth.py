from datetime import datetime, timedelta, timezone
from hashlib import sha256

import jwt

from models import User
from settings import settings


def get_hashed_password(password: str, secret: str = settings.secret) -> str:
    secret_password = secret + password
    return sha256(secret_password.encode()).hexdigest()


def validate_password(password: str, hashed_password: str) -> bool:
    if get_hashed_password(password) == hashed_password:
        return True
    return False


def issue_token(user: User, secret: str = settings.secret):
    payload = {
        "admin": user.is_admin,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=2),
    }
    token = jwt.encode(payload, key=secret, algorithm="HS256")
    return token


def validate_token(token: str, secret: str = settings.secret) -> dict:
    try:
        payload = jwt.decode(token, key=secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "signature has expired"}
    except jwt.InvalidTokenError:
        return {"error": "token is invalid"}
