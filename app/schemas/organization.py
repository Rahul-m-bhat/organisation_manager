from pydantic import BaseModel, EmailStr

class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str

class OrganizationGet(BaseModel):
    organization_name: str

class OrganizationResponse(BaseModel):
    organization_name: str
    admin_email: EmailStr
    message: str