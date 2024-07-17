from pydantic import BaseModel
from enum import Enum
from typing import List

class UserType(str, Enum):
    """
    Enum representing the type of a user.

    Attributes:
        FREE (str): Represents a free user.
        PREMIUM (str): Represents a premium user.
    """
    FREE = "free"
    PREMIUM = "premium"

class User(BaseModel):
    """
    Represents a user with a unique identifier, username, password, and user type.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        type (UserType): The type of the user (free or premium).
    """
    id: int
    username: str
    password: str
    type: UserType
