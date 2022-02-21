from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from matplotlib.pyplot import title
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

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

app.include_router(post.router, prefix="/posts", tags=["osts"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])