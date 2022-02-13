from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

@app.get("/posts")
def get_posts():
    return {"data":"Your posts"}

@app.post("/create_posts")
def create_posts(new_post:Post):
    print(new_post.published)
    return {"data": "New Post!!"}