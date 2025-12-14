import random
import time

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = 0


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            # password="",
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE CONNECTION WAS SUCCESSFULLY!")
        break
    except Exception as error:
        print("DATABASE CONNECTIOIN FAILED!!!")
        print("ERROR:", error)
        time.sleep(2)


my_posts = [
    {
        "title": "I like pizza!!!!",
        "content": "I really love pizza, especially pepperoni, it's the best!",
        "published": True,
        "rating": 5,
        "id": 1,
    },
    {
        "title": "look at my new car",
        "content": "I just bought a new car, it's a red convertible!",
        "published": False,
        "id": 2,
    },
    {
        "title": "testing this social media app",
        "content": "",
        "published": True,
        "rating": 3,
        "id": 3,
    },
]


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"post_detail": post}


def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get("/")
async def root():
    return {"message": "landing page"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    id: int = random.randint(1, 10000000000)
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts.append(post_dict)
    return {"data": post}


@app.get("/posts/{id}")
async def get_post(id: int, res: Response):
    finded_post = find_post(id)
    if not finded_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return finded_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    my_posts.pop(index)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
