from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host='localhost', database='social_media',
                                user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successfull!")
        break
    except Exception as e:
        print("Could not connect to the database")
        print("Error: ", e)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    # optional field set to default value
    published: bool = True


@app.get("/")
def get_user():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"posts": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s,%s,%s) RETURNING *""",
                   (payload.title, payload.content, payload.published))
    new_post = cursor.fetchone()
    # save the new record in the db
    conn.commit()
    return {"post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id)))
    deleted_post = cursor.fetchone()
    # save the changes to the db
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""",
                   (payload.title, payload.content, payload.published, str(id)))
    new_post = cursor.fetchone()
    # save the new record in the db
    conn.commit()

    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"posts": new_post}
