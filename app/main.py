from dataclasses import dataclass
from importlib.resources import contents
from logging import exception
from pyexpat import model
from time import sleep
from typing import Optional, List
from fastapi import Body, FastAPI, Response, responses, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        sleep(2)




@app.get("/")   
def root():
    return {"message": "Welcome to my pepega"}


@app.get("/posts", response_model= List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get('/posts/{id}', response_model= schema.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} was not found")
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id: {id} does not exist')
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message" : "post was succesfully deleted"}
    
@app.put('/posts/{id}', response_model= schema.Post)
def update_post(id:int, post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id: {id} does not exist')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return updated_post

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user:schema.UserCreate, db: Session = Depends(get_db)):

    #hash password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user