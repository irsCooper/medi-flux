from fastapi import HTTPException, status

class DatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Exception: Cannot insert data into table"
        )


class UnknowanDatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknowan Exception: Cannot insert data into table"
        )

class ConflictUnicueAttribute(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class RolesException(HTTPException):
    def __init__(self, roles):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Roles {', '.join(roles)} not found"
        )