from dataclasses import dataclass
from logging import exception
from time import sleep
from typing import Optional
from fastapi import Body, FastAPI, Response, responses, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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


my_posts = [{"title": "title of post 1", "content" : "content of post 1", "id": 1},
{"title": "food", "content" : "pizza", "id": 2} ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my pepega"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    cursor.execute("""select * from posts WHERE ID = (%s)""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} was not found")
    return {"post_detail": post }
    return {"data": posts}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE ID = (%s) returning *""", ((str(id),)))
    deleted = cursor.fetchone()
    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id: {id} does not exist')
    conn.commit()
    return {"message" : "post was succesfully deleted"}
    
@app.put('/posts/{id}')
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = (%s)  RETURNING *""",
    (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post with id: {id} does not exist')
    conn.commit()
    return {"data" : updated_post}
