from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.db.master_db_models import OrganizationMaster
from app.models.users import User, OrgBase
from app.core.security import get_password_hash
import os

def create_organization_and_admin(
    db_master: Session,
    org_name: str,
    admin_email: str,
    admin_password: str
):
    
    db_filename = f"{org_name.lower().replace(' ', '_').replace('.', '')}.db"
    dynamic_db_path = os.path.join(os.getcwd(), db_filename) # Get absolute path
    dynamic_db_connection_string = f"sqlite:///{dynamic_db_path}"

    db_org = OrganizationMaster(
        organization_name=org_name,
        admin_email=admin_email,
        db_connection_string=dynamic_db_connection_string
    )
    db_master.add(db_org)
    db_master.commit()
    db_master.refresh(db_org)

    # Initializing the dynamic database for the new organization
    dynamic_engine = create_engine(dynamic_db_connection_string)
    OrgBase.metadata.create_all(bind=dynamic_engine)

    # Creating the admin user in the dynamic database
    DynamicSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dynamic_engine)
    db_org_specific = DynamicSessionLocal()
    try:
        hashed_password = get_password_hash(admin_password)
        admin_user = User(email=admin_email, hashed_password=hashed_password, is_admin=True)
        db_org_specific.add(admin_user)
        db_org_specific.commit()
        db_org_specific.refresh(admin_user)
    finally:
        db_org_specific.close()

    return db_org

def get_organization_by_name(db_master: Session, organization_name: str):
    return db_master.query(OrganizationMaster).filter(
        OrganizationMaster.organization_name == organization_name
    ).first()

def get_organization_by_admin_email(db_master: Session, admin_email: str):
    return db_master.query(OrganizationMaster).filter(
        OrganizationMaster.admin_email == admin_email
    ).first()