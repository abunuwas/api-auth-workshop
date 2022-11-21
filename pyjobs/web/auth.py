import requests
from jose import jwt, jws

public_keys = requests.get(
    "https://coffeemesh-dev.eu.auth0.com/.well-known/jwks.json"
).json()["keys"]


def _get_certificate_for_key(kid):
    for key in public_keys:
        if key["kid"] == kid:
            return key
    raise Exception(f"No matching key found for kid {kid}")


def validate_token(token):
    unverified_headers = jws.get_unverified_headers(token)
    return jwt.decode(
        token=token,
        key=_get_certificate_for_key(unverified_headers["kid"]),
        audience="http://127.0.0.1:8000/jobs",
        algorithms=["RS256"],
    )
