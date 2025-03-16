from fastapi import APIRouter

from app.api.routes import posts, tokens, users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(posts.router, prefix="/posts", tags=["Posts"])
router.include_router(tokens.router, prefix="/tokens", tags=["Tokens"])
