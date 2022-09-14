from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

x509_certificate = load_pem_x509_certificate(
    Path("public_key.pem").read_text().encode()
).public_key()


def validate_token(token):
    unverified_headers = jwt.get_unverified_header(token)
    return jwt.decode(
        token,
        key=x509_certificate,
        algorithms=unverified_headers["alg"],
        audience="https://pyjobs.works/jobs"
    )

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucHlqb2JzLndvcmtzIiwic3ViIjoiMjM0NTY1NDMiLCJhdWQiOiJodHRwczovL3B5am9icy53b3Jrcy9qb2JzIiwiaWF0IjoxNjYyOTgxNjIyLjIxNzc3NywiZXhwIjoxNjYyOTg1MjIyLjIxNzc3N30.nfuocC1EEoUifMpsjHcDMT4dYU9GoOmsk1R_GBlSlH_6j_wcMO753nj0UnjoRxiYMuPBvHkF8-7OtTMbPL00VhU0px8AVjVlhyFZ3zNOpLj5ppXQW845jfRcPfChonkobHZcc0S7QwRqWunbFDcOhbcOAmVwsHt3lkVFZDp0-TRt7GtjdcraWfUujckysuoJg6yaTCzSVyW2Ihp6t67WqXMwZstIJo1ewkiG-e1KqxNR0vGb9TN1_1J9GvF63gmv9PUlswZ-gtQoJpPJPoidotJrN2_GJpS1lsA3h_p_1zVmZD5Jjulf8MDbYI2QaBWT9A9sgRUWszZn58HxXVyjbg"

print(validate_token(token))
