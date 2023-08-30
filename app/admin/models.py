from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def is_password_correct(self, password: str) -> bool:
        return self.hash_password(password) == self.password

    @classmethod
    def admin_from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])

