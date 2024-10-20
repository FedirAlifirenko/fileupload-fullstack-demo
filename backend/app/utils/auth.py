from typing import TypedDict

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {
    "alice": pwd_context.hash("alice_password"),
    "bob": pwd_context.hash("bob_password"),
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
