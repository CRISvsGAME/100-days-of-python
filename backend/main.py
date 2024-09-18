"""Main Backend"""

import uuid
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.middleware("http")
async def request_log(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Request Log"""

    request_id = request.cookies.get("request_id") or "request_id"
    request_count = request.cookies.get("request_count") or "0"

    if not valid_uuid4(request_id):
        request_id = str(uuid.uuid4())

    if not valid_int(request_count):
        request_count = "0"

    print("#" * 80)

    print("REQUEST:")
    print(f"{request.method} {request.url}")

    print("HEADERS:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    print("COOKIES:")
    for cookie, value in request.cookies.items():
        print(f"{cookie}: {value}")

    response: Response = await call_next(request)

    response.set_cookie(
        key="request_id",
        value=request_id,
        max_age=60 * 60 * 24 * 365,
        secure=True,
        httponly=True,
        samesite="strict",
    )

    response.set_cookie(
        key="request_count",
        value=str(int(request_count) + 1),
        max_age=60 * 60 * 24 * 365,
        secure=True,
        httponly=True,
        samesite="strict",
    )

    return response


@app.get("/")
async def root() -> dict[str, str]:
    """Root Endpoint"""
    return {"message": "Hello World"}


def valid_uuid4(uuid4: str) -> bool:
    """Valid UUID4"""
    try:
        uuid.UUID(uuid4, version=4)
        return True
    except ValueError:
        return False


def valid_int(value: str) -> bool:
    """Valid Int"""
    try:
        int(value)
        return True
    except ValueError:
        return False
