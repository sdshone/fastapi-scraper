from fastapi import HTTPException, Header

async def authenticate(x_token: str = Header(...)):
    """
    Authenticates the request based on the provided token.
    Raises HTTPException if the provided token is not valid.
    """
    # Define the expected token value
    expected_token = "secret-token"

    # Check if the provided token matches the expected token
    if x_token != expected_token:
        # Raise an HTTP 401 Unauthorized exception if the token does not match
        raise HTTPException(status_code=401, detail="Unauthorized")
