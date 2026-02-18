from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from db import engine, get_db
from schemas.user_schemas import UserCreate, User
from routes import user_routes

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)

@app.get("/")
def hello_world():
    return {"Hello World!"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[User])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user