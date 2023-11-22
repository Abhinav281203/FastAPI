from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"data": "base path"}


# Expected object format to the endpoint
class blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


# Using the type as blog
@app.post("/blog")
def create_blog(request: blog):
    return {"data": f"blog created {request.title}, {request.body}"}


# To run it as a general py file
# if __name__ == "__main__":
#     uvicorn.run(app, host = '127.0.0.1', port = 8000)
