from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
from typing import List

from app.schemas.user import User, UserType
from app.services.auth_service import create_user, authenticate_user, UserNameAlreadyExistsError, InvalidPasswordError
from app.utils.auth_utils import create_access_token, get_user_from_token


router = APIRouter(
    prefix="/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/create-user", response_model=User)
def create_new_user(username: str, password: str, user_type: UserType):
    """
    Create a new user.

    This endpoint creates a new user with the provided username, password, and user type.
    
    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        user_type (UserType): The type of the user (free or premium).

    Returns:
        User: The created user.

    Raises:
        HTTPException: If the username already exists (status code 409), 
        if the password is invalid (status code 400), or for any other error (status code 500).
    """
    try:
        return create_user(username, password, user_type)
    except UserNameAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidPasswordError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in the user.

    This endpoint authenticates a user and returns an access token if the credentials are valid.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.

    Returns:
        dict: A dictionary containing the access token, token type, and expiration time in minutes.

    Raises:
        HTTPException: If the username or password is incorrect (status code 400).
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token, expire = create_access_token(data={"sub": user.username})
    expire_in_minutes = int((expire - datetime.utcnow()).total_seconds() / 60)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": expire_in_minutes}

@router.get("/{token}", response_model=User)
def get_user_by_token(token: str):
    """
    Get user by token.

    This endpoint retrieves a user based on the provided JWT token.
    
    Args:
        token (str): The JWT token of the user.

    Returns:
        User: The user associated with the token.

    Raises:
        HTTPException: If the user is not found (status code 404).
    """
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user