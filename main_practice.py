from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

users = [
    {
        "id": 1,
        "name": "Ali"
    },
    {
        "id": 2,
        "name": "Daniyar"
    }
]

next_id = 3

class UserResponse(BaseModel):
    id: int
    name: str

@app.get("/users", response_model=list[UserResponse])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)

@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate):
    global next_id
    user = {
        "id": next_id,
        "name": user.name
    }
    users.append(user)
    next_id += 1
    return user
class UserUpdate(BaseModel):
    name: str = Field(min_length=2,max_length=30)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user: UserUpdate, user_id: int):
    for user_data in users:
        if user_data["id"] == user_id:
            user_data["name"] = user.name
            return user_data
    raise HTTPException(status_code=404, detail="User not found")

class MessageResponse(BaseModel):
    message: str

@app.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
