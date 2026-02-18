from pydantic import BaseModel, EmailStr

# Base fields
class UserBase(BaseModel):
    email: EmailStr
    name: str

# Fields needed for creating a user (Signup)
class UserCreate(UserBase):
    password: str

# Fields returned to the frontend (Response)
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models