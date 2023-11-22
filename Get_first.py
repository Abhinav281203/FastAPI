from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog list"}


@app.get("/about")
def about():
    return {"data": "About Abhinav"}


# http://127.0.0.1:8000/blog?limit=4&published=false
@app.get("/blog")
def show(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from db"}
    else:
        return {"data": f"{limit} blogs from from db"}
