from .utils import hash_password, verify_password
_users = {
    "abmishra": {"username":"abmishra","hashed":hash_password("password"),"role":"admin"},
    "abinash": {"username":"abinash","hashed":hash_password("password"),"role":"customer"},
    "rahul": {"username":"rahul","hashed":hash_password("password"),"role":"admin"},
    "rahul1": {"username":"rahul1","hashed":hash_password("password"),"role":"customer"},
    "arun": {"username":"arun","hashed":hash_password("password"),"role":"admin"},
    "admin": {"username":"admin","hashed":hash_password("password"),"role":"admin"},
}
def get_user_by_username(u): return _users.get(u)
def authenticate(u,p):
    user = get_user_by_username(u)
    return user if user and verify_password(p, user["hashed"]) else None
