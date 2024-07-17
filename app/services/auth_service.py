import json

from app.schemas.user import User, UserType
from app.utils.auth_utils import read_users, get_password_hash, is_username_taken, validate_password, verify_password

class UserNameAlreadyExistsError(Exception):
    """
    Exception raised when the username is already taken.

    Attributes:
        username (str): The username that is already taken.
        message (str): The error message indicating the username is already taken.
    """
    def __init__(self, username: str):
        self.message = f"Username '{username}' is already taken"
        super().__init__(self.message)

class InvalidPasswordError(Exception):
    """
    Exception raised for invalid passwords.

    Attributes:
        message (str): The error message indicating the password criteria are not met.
    """
    def __init__(self):
        self.message = "Password must be at least 6 characters long and contain at least one uppercase letter"
        super().__init__(self.message)

def create_user(username: str, password: str, user_type: UserType):
    """
    Create a new user.

    This function creates a new user with the provided username, password, and user type.
    It raises an exception if the username is already taken or if the password is invalid.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        user_type (UserType): The type of the user (free or premium).

    Returns:
        User: The created user.

    Raises:
        UserNameAlreadyExistsError: If the username is already taken.
        InvalidPasswordError: If the password is invalid.
    """
    if is_username_taken(username):
        raise UserNameAlreadyExistsError(username)
    if not validate_password(password):
        raise InvalidPasswordError()
    users = read_users()
    new_user = User(
        id=len(users) + 1,
        username=username,
        password=get_password_hash(password),
        type=user_type
    )
    users.append(new_user)
    with open('data/users_data.json', 'w') as file:
        json.dump([user.model_dump() for user in users], file, indent=4)
    return new_user

def authenticate_user(username: str, password: str) -> User:
    """
    Authenticate a user.

    This function authenticates a user by checking the provided username and password.
    It returns the user if authentication is successful.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The authenticated user, or None if authentication fails.
    """
    users = read_users()
    user = next((user for user in users if user.username == username), None)
    if user and verify_password(password, user.password):
        return user
    return None
