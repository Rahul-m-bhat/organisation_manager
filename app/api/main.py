from fastapi import FastAPI
from app.db.master_db_models import init_master_db
from app.api.endpoints import organization, admin
import os

app = FastAPI(
    title="Organization Management API",
    description="API for managing organizations and their admins",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    # Ensure the directory for master.db exists (if using relative path)
    db_dir = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'master.db')))
    os.makedirs(db_dir, exist_ok=True)
    init_master_db()

app.include_router(organization.router, prefix="/org", tags=["Organization"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])