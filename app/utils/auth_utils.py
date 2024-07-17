import json
import re
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional, List

from app.schemas.user import User

SECRET_KEY = "e50fa47bbc0247dcd243ab71c9a95f5a7f63d5b879a196237e442b9207b9a945"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def read_users() -> List[User]:
    """
    Retrieve all users from the JSON file.

    This function reads users data from the 'data/users_data.json' file and converts it into a list of User objects.

    Returns:
        List[User]: A list of User objects.
    """
    with open('data/users_data.json', 'r') as file:
        users_data = json.load(file)
        return [User(**user) for user in users_data]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    This function creates a JWT access token with the provided data and expiration delta.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The time delta for the token's expiration. Defaults to 30 minutes.

    Returns:
        Tuple[str, datetime]: The encoded JWT token and its expiration datetime.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    This function hashes a plain password using bcrypt.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def is_username_taken(username: str) -> bool:
    """
    Check if a username is already taken.

    This function checks if the given username is already taken by any user.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username is taken, False otherwise.
    """
    users = read_users()
    return any(user.username == username for user in users)

def validate_password(password: str) -> bool:
    """
    Validate a password.

    This function validates the password to ensure it meets the required criteria: at least 6 characters long and contains at least one uppercase letter.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password.

    This function verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_user_from_token(token: str) -> Optional[User]:
    """
    Retrieve a user from a JWT token.

    This function decodes the JWT token to get the username and fetches the corresponding user.
    It also checks if the token is expired.

    Args:
        token (str): The JWT token.

    Returns:
        Optional[User]: The user associated with the token, or None if the user is not found or the token is invalid.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        
        if username is None or exp is None:
            return None

        if datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        return next((user for user in read_users() if user.username == username), None)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")