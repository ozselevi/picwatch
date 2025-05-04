from pydantic import BaseModel


class ImageCreate(BaseModel):
    filename: str
    description: str
