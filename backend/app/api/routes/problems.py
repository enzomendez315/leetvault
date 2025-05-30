import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    Problem,
    ProblemCreate,
    ProblemPublic,
    ProblemUpdate,
    ProblemsPublic
)

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/", response_model=ProblemsPublic)
def get_problems(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve a paginated list of all LeetCode problems (admin only).

    - **session**: Database session dependency.
    - **current_user**: The authenticated user making the request.
    - **skip**: Number of items to skip for pagination.
    - **limit**: Maximum number of items to return.

    Only superusers are allowed to access this endpoint.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Problem)
        count = session.exec(count_statement).one()
        statement = select(Problem).offset(skip).limit(limit)
        problems = session.exec(statement).all()
    else:
        raise HTTPException(
            status_code=403, detail="Only admins can see this page"
        )
    return ProblemsPublic(data=problems, count=count)


@router.get("/{id}", response_model=ProblemPublic)
def get_problem(
        session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Retrieve a single LeetCode problem by its ID (admin only).

    - **session**: Database session dependency.
    - **current_user**: The authenticated user making the request.
    - **id**: UUID of the problem to retrieve.

    Only superusers are allowed to access this endpoint.
    """
    problem = session.get(Problem, id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Only admins can see this page"
        )
    return problem


@router.post("/", response_model=ProblemPublic)
def create_problem(
        *, session: SessionDep, current_user: CurrentUser, problem_in: ProblemCreate
) -> Any:
    """
    Create a new LeetCode problem (admin only).

    - **session**: Database session dependency.
    - **current_user**: The authenticated user making the request.
    - **problem_in**: Data required to create the problem.

    Only superusers are allowed to access this endpoint.
    """
    problem = Problem.model_validate(problem_in)
    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem


@router.put("/{id}", response_model=ProblemPublic)
def update_problem(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        problem_in: ProblemUpdate
) -> Any:
    """
    Update an existing LeetCode problem by its ID (admin only).

    - **session**: Database session dependency.
    - **current_user**: The authenticated user making the request.
    - **id**: UUID of the problem to update.
    - **problem_in**: Fields to update.

    Only superusers are allowed to access this endpoint.
    """
    problem = session.get(Problem, id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Only admins can see this page"
        )
    update_dict = problem_in.model_dump(exclude_unset=True)
    problem.sqlmodel_update(update_dict)
    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem


@router.delete("/{id}")
def delete_problem(
        session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a LeetCode problem by its ID (admin only).

    - **session**: Database session dependency.
    - **current_user**: The authenticated user making the request.
    - **id**: UUID of the problem to delete.

    Only superusers are allowed to access this endpoint.
    """
    problem = session.get(Problem, id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Only admins can see this page"
        )
    session.delete(problem)
    session.commit()
    return Message(message="Problem deleted")