from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Check health"])
async def checkhealth():
    return {"status":200}

@router.get("/", tags=["Check health"])
async def entrypoint():
    return {"message" : "Welcome to Falcon-X Platform"}