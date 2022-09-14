from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives._serialization import Encoding, PublicFormat
from jose import jwt

private_key = Path("private_key.pem").read_text()


def generate_token():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": "https://auth.pyjobs.works",
        "sub": "23456543",
        "aud": "https://pyjobs.works/jobs",
        "iat": now.timestamp(),
        "exp": (now + timedelta(hours=1)).timestamp()
    }

    return jwt.encode(claims=payload, key=private_key, algorithm="RS256")


private_key_loaded = serialization.load_pem_private_key(
    data=private_key.encode(), password=None
)

print("*** PUBLIC KEY ***")
print(private_key_loaded.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).decode())

print()

print("*** TOKEN ***")
print(generate_token())
