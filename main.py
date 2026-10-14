from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db_orm import get_db
from models import User
from user_repository import (
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
)

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

@app.get("/")
def home():
    return {"message": "API is working!"}


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

@app.post("/users", response_model=UserResponse, status_code=201)
def create_new_user(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        with db.begin():
            user = User(
                name=user_data.name,
                email=user_data.email,
            )
            db.add(user)

        return user

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        with db.begin():
            user = update_user_by_id(
                db,
                user_id,
                user_data.name,
                user_data.email,
            )

            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )

        return user

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

@app.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    with db.begin():
        deleted = delete_user_by_id(db, user_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
