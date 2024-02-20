from fastapi import HTTPException, status

InvalidTokenHTTPException = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
EmailAlreadyInUseHTTPException = HTTPException(status.HTTP_400_BAD_REQUEST, "Email already in use")
InvalidCredentialsHTTPException = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
InvalidClassroomCodeHTTPException = HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid classroom code")
ClassroomNotFoundHTTPException = HTTPException(status.HTTP_404_NOT_FOUND, "Classrooom not found")
NotInClassroomHTTPException = HTTPException(status.HTTP_403_FORBIDDEN, "Not in that classroom")
AlreadyInClassroomHTTPException = HTTPException(status.HTTP_400_BAD_REQUEST, "Already in classroom")