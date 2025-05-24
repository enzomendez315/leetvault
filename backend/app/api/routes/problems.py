import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Problem, ProblemCreate, ProblemPublic, ProblemsPublic

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/", response_model=ProblemsPublic)
def get_problems(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 100
) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Problem)
        count = session.exec(count_statement).one()
        statement = select(Problem).offset(skip).limit(limit)
        problems = session.exec(statement).all()
        
    return ProblemsPublic(data=problems, count=count)


@router.get("/{id}")
def get_problem(session: SessionDep, current_user: CurrentUser, id: uuid.UUID):
    pass


@router.post("/")
def create_problem():
    pass