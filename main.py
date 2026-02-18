from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from db import engine, get_db

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello World!"}
    

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    db_user = models.User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user