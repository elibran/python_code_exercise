from typing import Optional, Callable
from fastapi import Depends, HTTPException, Request # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore
from jose import jwt, JWTError # type: ignore
from .security import SECRET_KEY, ALGORITHM
from .users import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    username: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")
    if not username or not role:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    if not get_user_by_username(username):
        raise HTTPException(status_code=401, detail="User not found")
    return {"username": username, "role": role}

def role_required(required_role: str, allow_admin_on_get: bool = True) -> Callable:
    """
    - Exact role match is required by default.
    - If `allow_admin_on_get` is True (default), users with role `admin` are allowed to
      access any GET endpoint, even when `required_role` differs.
    """
    async def _checker(request: Request, current=Depends(get_current_user)):
        if current["role"].lower() == required_role.lower():
            return current
        if allow_admin_on_get and request.method.upper() == "GET" and current["role"].lower() == "admin":
            return current
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return _checker
