from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import Message, NewPassword, Token, TokenPayload, UserPublic
from app.utils import (
    generate_reset_password_email,
    generate_reset_password_token,
    send_email,
    verify_reset_password_token,
)

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2-compatible login to obtain an access token for authenticated requests.

    - **session**: Database session dependency.
    - **form_data**: Login form data with `username` and `password`.

    Returns an access token if authentication is successful.
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test the validity of an access token by retrieving the current user.

    - **current_user**: The user extracted from the token.

    Returns the authenticated user if the token is valid.
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Send a password recovery email to the specified address.

    - **email**: Email of the user requesting password reset.
    - **session**: Database session dependency.

    Sends a recovery link if the user exists.
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_token = generate_reset_password_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content
    )

    return Message(message="Password recovery email sent")


@router.post("reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset the password using a valid token.

    - **session**: Database session dependency.
    - **body**: Payload containing the new password and token.

    Updates the user's password if the token is valid.
    """
    email = verify_reset_password_token(token=body.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password

    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=HTMLResponse
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    Generate the HTML content for a password recovery email.

    - **email**: Email address of the user.
    - **session**: Database session dependency.

    Returns the HTML email content and subject header (admin only).
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_token = generate_reset_password_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(content=email_data.html_content, headers={"subject:": email_data.subject})