import os

from fastapi import FastAPI
from jose import ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from pyjobs.web.api.api import router as jobs_router
from pyjobs.web.auth import validate_token

server = FastAPI(debug=True)

server.include_router(jobs_router)


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if os.getenv("AUTH_ON", "False") != "True":
            request.state.user_id = "test"
            return await call_next(request)

        if request.url.path in ["/docs", "/openapi.json", "/redocs"]:
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                }
            )
        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = validate_token(auth_token)
        except (
            ExpiredSignatureError,
            JWTError,
            JWTClaimsError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)}
            )
        else:
            request.state.user_id = int(token_payload["sub"])
        return await call_next(request)


server.add_middleware(AuthorizeRequestMiddleware)

