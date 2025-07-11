from fastapi import FastAPI, Depends, HTTPException
from .api import router as api_router
from .auth import get_current_user

app = FastAPI(title="Cloud Security API")

app.include_router(api_router, prefix="/api", dependencies=[Depends(get_current_user)])