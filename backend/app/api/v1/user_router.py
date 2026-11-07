from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

# Define a clean resource prefix
router = APIRouter(prefix="/users", tags=["Users V1"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.register_user(user_in)
