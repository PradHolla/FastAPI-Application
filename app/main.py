from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from matplotlib.pyplot import title
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # print(posts)
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")

    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()
    del_post = db.query(models.Post).filter(models.Post.id == id)
    if del_post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")
    
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    first_post = post_query.first()
    if first_post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user