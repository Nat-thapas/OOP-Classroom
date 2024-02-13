from fastapi import HTTPException, status

InvalidTokenHTTPException = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
EmailAlreadyInUseHTTPException = HTTPException(status.HTTP_400_BAD_REQUEST, "Email already in use")
InvalidCredentialsHTTPException = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")