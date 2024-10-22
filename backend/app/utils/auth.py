from typing import TypedDict

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {
    "admin": pwd_context.hash("admin"),
    "guest": pwd_context.hash("guest"),
    "test": pwd_context.hash("test"),
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class User(TypedDict):
    username: str
    hashed_password: str


def get_user(username: str) -> User | None:
    if username in users_db:
        return {"username": username, "hashed_password": users_db[username]}
    return None
