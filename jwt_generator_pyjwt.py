from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives._serialization import Encoding, PublicFormat

private_key = Path("private_key.pem").read_text()

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.pyjobs.works",
    "sub": "1",
    "aud": "https://pyjobs.works/jobs",
    "iat": now.timestamp(),
    "exp": (now + timedelta(hours=1)).timestamp()
}

private_key_loaded = serialization.load_pem_private_key(
    data=private_key.encode(), password=None
)

token = jwt.encode(payload=payload, key=private_key_loaded, algorithm="RS256")

print("*** PUBLIC KEY ***")
print(private_key_loaded.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).decode())

print()

print("*** TOKEN ***")
print(token)

