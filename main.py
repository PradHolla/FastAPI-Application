from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
app = FastAPI()


my_posts = [{"title": "Top laptops", "content": "Amazing laptops of this year", "published": True, "rating": 7.4, "id": 1},
            {"title": "Top restaurant chains", "content": "Amazing restaurant chains you have to try", "published": True, "rating": 7.1, "id": 2},]
@app.get("/")
def root():
    return {"message":"Hello World"}

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:Optional[float] = None

def find_post(id):
    for post in my_posts:
        if post["id"] == (id):
            return post

@app.get("/posts")
def get_posts():
    return {"data":"Your posts"}

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