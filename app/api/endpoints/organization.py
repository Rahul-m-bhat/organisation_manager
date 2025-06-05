from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.organization import OrganizationCreate, OrganizationGet, OrganizationResponse
from app.crud import organization as crud_org
from app.db.database import get_master_db


router = APIRouter()

@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    org_in: OrganizationCreate,
    db_master: Session = Depends(get_master_db)
):
    """
    Create an Organization with an admin user and a dynamic database.
    """
    existing_org = crud_org.get_organization_by_name(db_master, org_in.organization_name)
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this name already exists"
        )
    existing_admin = crud_org.get_organization_by_admin_email(db_master, org_in.email)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email is already associated with an organization"
        )

    organization = crud_org.create_organization_and_admin(
        db_master=db_master,
        org_name=org_in.organization_name,
        admin_email=org_in.email,
        admin_password=org_in.password
    )
    return OrganizationResponse(
        organization_name=organization.organization_name,
        admin_email=organization.admin_email,
        message="Organization and admin created successfully"
    )

@router.get("/get", response_model=OrganizationResponse)
def get_organization_by_name(
    org_get: OrganizationGet = Depends(),
    db_master: Session = Depends(get_master_db)
):
    """
    Get organization information by name.
    """
    organization = crud_org.get_organization_by_name(db_master, org_get.organization_name)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return OrganizationResponse(
        organization_name=organization.organization_name,
        admin_email=organization.admin_email,
        message="Organization found"
    )