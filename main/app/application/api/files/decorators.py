from functools import wraps

from fastapi import HTTPException, status

from domain.exceptions.base import ApplicationException


def handle_exceptions(handle):
    @wraps(handle)
    async def wrapper(*args, **kwargs):
        try:
            result = await handle(*args, **kwargs)
        except ApplicationException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": exception.message},
            )
        return result

    return wrapper
