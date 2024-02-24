from app import app

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import os
import secrets

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

security = HTTPBasic()

def check_local(ip: str) -> bool:
    print(ip)
    # предполагая, что локальная сеть имеет IP-адреса начинающиеся с '192.168.'
    return ip.startswith("192.168.3.")

def get_current_username(credentials: Optional[HTTPBasicCredentials] = Depends(security), request: Request = None) -> str:
    if request and check_local(request.client.host):
        return "local_user"  # для локального пользователя вернем допустимый username

    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = LOGIN.encode("utf8")
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = PASSWORD.encode("utf8")
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
