import uuid

from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = False
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)

# Properties received via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Problem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: int = Field(unique=True, index=True)
    name: str = Field(index=True, max_length=255)
    description: str
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, index=True)

class SolvedProblemSet(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: int = Field(unique=True, index=True)