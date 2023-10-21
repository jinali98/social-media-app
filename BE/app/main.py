from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # optional field set to default value
    published: bool = True
    # optional value
    rating: Optional[int] = None


my_posts = [{
    "id": 1,
    "title": "Fast api",
    "content": "This is the post content",
    "published": True,
    "rating": None
},
    {
    "id": 2,
    "title": "I Love Pizza",
    "content": "This is the post content",
    "published": True,
    "rating": None
}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def get_user():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"posts": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    # converting to a python dictionary
    new_post = payload.model_dump()
    new_post["id"] = randrange(0, 1000)
    my_posts.append(new_post)
    return {"post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index(id)

    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    my_posts.pop(post_index)


@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    post_index = find_post_index(id)
    print(post_index)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_dict = payload.model_dump()
    post_dict['id'] = id
    my_posts[post_index] = post_dict
    return {"posts": post_dict}
