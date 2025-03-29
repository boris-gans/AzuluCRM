from fastapi import Header, HTTPException, Depends, status
import os
from typing import Optional

# Get admin password from environment variable or use default (for development only)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

async def verify_admin(x_admin_password: Optional[str] = Header(None)) -> bool:
    """Verify that the admin password header matches the expected value"""
    if not x_admin_password or x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Admin-Password"},
        )
    return True 