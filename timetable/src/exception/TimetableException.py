from fastapi import HTTPException, status

class TimetableNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetabe not found"
        )


class DatatimeOnFormError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'to' field should be larger than the 'from' field"
        )