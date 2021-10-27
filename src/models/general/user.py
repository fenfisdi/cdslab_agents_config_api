from enum import Enum


class UserRole(Enum):
    ROOT: str = 'root'
    ADMIN: str = 'admin'
    USER: str = 'user'
