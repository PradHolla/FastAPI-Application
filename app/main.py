from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="x", user="x", password="x", cursor_factory=RealDictCursor)
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
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with ID: {id} not found"}
    return {"post_details": post}
    # for post in my_posts:
    #     if post["id"] == id:
    #         return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")
    
    my_posts.remove(post)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Post with ID: {id} not found")

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}