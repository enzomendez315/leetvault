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


# Properties received via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


# Database model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(SQLModel):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ProblemBase(SQLModel):
    number: int = Field(unique=True, index=True)
    name: str = Field(index=True, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, index=True)


# Properties to receive on problem creation
class ProblemCreate(ProblemBase):
    pass


# Properties to receive on problem update
class ProblemUpdate(ProblemBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model
class Problem(ProblemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Properties to return via API, id is always required
class ProblemPublic(ProblemBase):
    id: uuid.UUID


class ProblemsPublic(SQLModel):
    data: list[ProblemPublic]
    count: int


class ProblemSolved(ProblemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner: User = Relationship(back_populates="users", cascade_delete=True)


class EmailData(SQLModel):
    html_content: str
    subject: str


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "Bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)