# organisation_manager

## Create Organization
  """Create an Organization with an admin user and a dynamic database."""

    URL : http://localhost:8000/org/create
    METHOD : POST
    REQUEST PAYLOAD : {
      "email": "user@example.com",
      "password": "string",
      "organization_name": "string"
      }


## Get Organization By Name
  """Get organization information by name."""

    URL : http://localhost:8000/org/get
    METHOD : GET
    RESPONSE PAYLOAD : {
      "organization_name": "string",
      "admin_email": "user@example.com",
      "message": "string"
    }


## Admin Login
  """Admin login to get a JWT token. The email provided must be the admin email associated with an organization."""
  
    URL : http://localhost:8000/admin/login
    METHOD : POST
    RESPONSE PAYLOAD : {
      "access_token": "string",
      "token_type": "bearer"
    }

