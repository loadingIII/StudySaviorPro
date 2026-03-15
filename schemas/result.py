from typing import Optional, Any

from pydantic import BaseModel


class Result(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None


def success_response(data=None, message: str="Success") -> Result:
    result = Result(code=1, message=message, data=data)
    return result

def error_response(message: str="Error", data=None) -> Result:
    result = Result(code=0, message=message, data=data)
    return result