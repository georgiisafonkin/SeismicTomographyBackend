from fastapi import APIRouter

from src.geo.models.schemas.users import Users

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/register", response_model=Users)
def register_user(user: Users, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db=db, user=user)

# TODO fix it