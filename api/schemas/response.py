from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: int
    data: dict | list | None = None
    message: str | None = None
