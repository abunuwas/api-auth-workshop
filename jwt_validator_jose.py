from pathlib import Path

from jose import jwt, jws

public_certificate = Path("public_key.pem").read_text()


def validate_token(token):
    unverified_headers = jws.get_unverified_header(token)
    return jwt.decode(
        token=token,
        key=public_certificate,
        audience="https://pyjobs.works/jobs",
        algorithms=unverified_headers["alg"]
    )

# token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucHlqb2JzLndvcmtzIiwic3ViIjoiMjM0NTY1NDMiLCJhdWQiOiJodHRwczovL3B5am9icy53b3Jrcy9qb2JzIiwiaWF0IjoxNjYyOTgxMjMyLjQ3OTEsImV4cCI6MTY2Mjk4NDgzMi40NzkxfQ.ReddaZ-nyTBjvVJ9qJ8SIbj0fKmZFyJ8ADkckkshaJFQmYjxqiL53z_-_r_QIpcJDVxH6mU5FAGZXXqg5jjbN7MCeNMgCiD4fRTz12KM6CQxg489wH8BOwLWI7-3XdbOxLKu6skghFpBWZohX5Nsv8A5HQhPi0zqFiTlINkf_iSb0qoK-dYE9Vum6Cc7FeZ46tSJHJbXyDFWDfwqFrr3DaPTXudE0-6upP4bl4BZ0hkWtOEG9VuaQd8ORmiRxf465s7Q0bSjM6m6Am15IqJcDc_YAv6lHravro8yj2Hp4cvsC0nsfRE1ww3eaixVoDIitI-QM59YS6Uq3FsD5XPm-A"
#
# print(validate_token(token))
