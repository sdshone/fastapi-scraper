from fastapi import HTTPException, Header

async def authenticate(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
