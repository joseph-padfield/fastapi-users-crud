from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Users CRUD API",
    description="A basic FastAPI CRUD back end using SQLite and SQLAlchemy.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Users CRUD API is running."}

@app.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    db_user = models.User(
        name=user.name,
        email=user.email,
        is_active=user.is_active
)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users/", 
        response_model=list[schemas.UserResponse],
)

def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = (
        db.query(models.User)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return users

@app.get("/users/{user_id}",
        response_model=schemas.UserResponse
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user

@app.put("/users/{user_id}",
        response_model=schemas.UserResponse
)

def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_user = (
            db.query(models.User)
            .filter(models.User.email == update_data["email"])
            .filter(models.User.id != user_id)
            .first()
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another user with this email already exists."
            )
    
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)

def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    db.delete(user)
    db.commit()

    return None