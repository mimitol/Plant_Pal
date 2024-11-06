from fastapi import HTTPException
import asyncio
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class DBConnectionError(Exception):
    """Raised when there is an error connecting to the database."""

    def __init__(self, message="Error connecting to the database"):
        self.message = message
        super().__init__(self.message)

class InvalidLoginError(Exception):
    """Raised when a registered user attempts to login as a new user."""

    def __init__(self, message="Invalid login attempt, check your details or signup"):
        self.message = message
        super().__init__(self.message)

class InvalidSignupError(Exception):
    """Raised when a registered user attempts to login as a new user."""
    def __init__(self, message="you recognized as a registerd user,check your details or login"):
        self.message = message
        super().__init__(self.message)

class QueryExecutionError(Exception):
    """Raised when there is an error during query execution."""

    def __init__(self, message="An error occurred,try again"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(Exception):
    """Raised when there is an error during query execution."""

    def __init__(self, message="Invalid input, check and try again"):
        self.message = message
        super().__init__(self.message)


class AlreadyExistError(Exception):
    """Raised when there is an error during query execution."""

    def __init__(self, message="This item is already exists"):
        self.message = message
        super().__init__(self.message)


def exceptions_handler(ex: Exception):
    if isinstance(ex, DBConnectionError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error_code": "DB_CONNECTION_ERROR", "message": str(ex)})
    elif isinstance(ex, InvalidLoginError):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"error_code": "INVALID_LOGIN", "message": str(ex)})
    elif isinstance(ex, InvalidSignupError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error_code": "INVALID_SIGNUP", "message": str(ex)})
    elif isinstance(ex, QueryExecutionError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error_code": "QUERY_EXECUTION_ERROR", "message": str(ex)})
    elif isinstance(ex, InvalidInputError):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content={"error_code": "INVALID_INPUT", "message": str(ex)})
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error_code": "UNKNOWN_ERROR", "message": "An unexpected error occurred"})

