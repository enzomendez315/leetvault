from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Problem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: int = Field(unique=True, index=True)
    name: str = Field(index=True, max_length=255)
    description: str
    difficulty: Difficulty

class SolvedProblemSet(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: int = Field(unique=True, index=True)