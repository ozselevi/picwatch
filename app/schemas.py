from pydantic import BaseModel

class ImageCreate(BaseModel):
    filename: str
    description: str
    people_count: int

class ImageOut(ImageCreate):
    id: int

    class Config:
        orm_mode = True

class SubscriberCreate(BaseModel):
    email: str

class SubscriberOut(SubscriberCreate):
    id: int

    class Config:
        orm_mode = True
