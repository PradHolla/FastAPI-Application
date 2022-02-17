from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/sql")
def test_post(db: Session = Depends(get_db)):
    # posts = db.query(models.Post).all()
    return {"status:": "ok"}

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapiApp", user="postgres", password="cnhpnhcnh", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database!")
        break
    except Exception as e:
        print("Unable to connect to the database")
        print(e)
        time.sleep(3)


my_posts = [{"title": "Top laptops", "content": "Amazing laptops of this year", "published": True, "rating": 7.4, "id": 1},
            {"title": "Top restaurant chains", "content": "Amazing restaurant chains you have to try", "published": True, "rating": 7.1, "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == (id):
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == (id):
            return index

@app.get("/posts")
def get_posts():
    posts = cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")

    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id),))
    del_post = cursor.fetchone()
    conn.commit()
    if not del_post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")

    return {"data": updated_post}