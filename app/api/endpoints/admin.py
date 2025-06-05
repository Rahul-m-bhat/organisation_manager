from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.crud import users as crud_user
from app.crud import organization as crud_org
from app.core.security import verify_password, create_access_token, decode_access_token # Import decode_access_token
from app.db.database import get_master_db, get_organization_db_session

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

@router.post("/login", response_model=Token)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_master: Session = Depends(get_master_db)
):
    """
    Admin login to get a JWT token.
    The email provided must be the admin email associated with an organization.
    """
    organization_master = crud_org.get_organization_by_admin_email(db_master, form_data.username)
    if not organization_master:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password", # Generic message for security
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the dynamic DB session for this organization
    org_db_session_generator = get_organization_db_session(organization_master.db_connection_string)
    try:
        org_db: Session = next(org_db_session_generator)
    except StopIteration:
        raise HTTPException(status_code=500, detail="Could not establish organization database connection")

    try:
        user = crud_user.get_user_by_email(org_db, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not an admin",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user.email, "organization_name": organization_master.organization_name}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        org_db.close() # Ensure the session is closed



@router.get("/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db_master: Session = Depends(get_master_db)
):
    """Example of a protected endpoint (requires JWT)"""

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    organization_name = payload.get("organization_name")

    if not email or not organization_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token payload"
        )

    organization_master = crud_org.get_organization_by_name(db_master, organization_name)
    if not organization_master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found for token"
        )

    org_db_session_generator = get_organization_db_session(organization_master.db_connection_string)
    try:
        org_db: Session = next(org_db_session_generator)
    except StopIteration:
        raise HTTPException(status_code=500, detail="Could not establish organization database connection")

    try:
        user = crud_user.get_user_by_email(org_db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in organization"
            )
        return {"email": user.email, "is_admin": user.is_admin, "organization_name": organization_name}
    finally:
        org_db.close()