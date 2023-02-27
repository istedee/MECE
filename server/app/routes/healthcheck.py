from fastapi import APIRouter


router = APIRouter(
    responses={403: {"description": "Invalid credentials"}},
)


@router.get(
    "/ping",
    tags=["health-check"],
    responses={200: {"description": "Returns 'pong' as status check msg"}},
)
async def root():
    return {"message": "pong"}
