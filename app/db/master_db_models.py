from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

MASTER_DATABASE_URL = settings.MASTER_DATABASE_URL

Base = declarative_base()

class OrganizationMaster(Base):
    __tablename__ = "organization_master"

    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String, unique=True, index=True, nullable=False)
    admin_email = Column(String, unique=True, index=True, nullable=False)
    #organization's dynamic DB connecting string
    db_connection_string = Column(String, nullable=False)

# This engine and session will be used for the master database
master_engine = create_engine(MASTER_DATABASE_URL)
MasterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)

def init_master_db():
    """Creates master database tables if they don't exist."""
    print("[INFO] Initializing Master Database...")
    Base.metadata.create_all(bind=master_engine)
    print("[INFO] Master Database initialized.")