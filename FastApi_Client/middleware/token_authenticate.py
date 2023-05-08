import os
from fastapi import HTTPException, Header, status

# Mock authentication token. This should be replaced with a proper authentication mechanism.
AUTH_TOKEN = os.getenv("AUTH_TOKEN")


async def authenticate(authorization: str = Header(None)):
    """
    Authenticates the user based on the provided token.

    Args:
        authorization (str): Authorization header containing the authentication token.

    Raises:
        HTTPException: If the provided token is invalid.

    Returns:
        None.
    """
    if authorization is None or authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
