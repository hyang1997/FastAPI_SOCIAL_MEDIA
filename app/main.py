from dataclasses import dataclass
from importlib.resources import contents
from logging import exception
from pyexpat import model
from time import sleep
from turtle import pos
from typing import Optional, List
from fastapi import Body, FastAPI, Response, responses, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)