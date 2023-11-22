from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas
import models
from hashing import Hash
from database import engine, localsession
import token_my
import oauth2
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()


# Dealing with the Database
def get_db():
    db = localsession()
    try:
        yield db
    finally:
        db.close()


# Creating all the tables present in models.py if not existing in database
models.base.metadata.create_all(engine)

# need to add 'db : Session = Depends(get_db)' as parameter for endpoints dealing with db


@app.post("/login", tags=["Authentication"])
def auth(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == req.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Credentials"
        )
    if not Hash.verify(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password"
        )

    access_token = token_my.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Add a record to the database
@app.post("/addblogs", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def createblog(
    req: schemas.blog,
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    new_blog = models.blog(title=req.title, body=req.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all the records
@app.get(
    "/getblogs",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.blogwithoutid],
    tags=["Blogs"],
)
def getallblogs(
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    blogs = db.query(models.blog).all()
    return blogs


# Get specific record - WHERE clause
@app.get(
    "/getblogs/{id}",
    status_code=200,
    response_model=schemas.blogwithoutid,
    tags=["Blogs"],
)
def getablog(
    id,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    blog = db.query(models.blog).filter(models.blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} is not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': 'blog with id {id} is not found'}
    return blog


# Delete a record
@app.delete("/delblogs/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def deleteblog(
    id,
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    blog = db.query(models.blog).filter(models.blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} is not found",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "deleted"}


# Update a record
@app.put("/updateblogs/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def updateblog(
    id,
    req: schemas.blog,
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    blog = db.query(models.blog).filter(models.blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} is not found",
        )
    blog.update(req)
    db.commit()
    return {"detail": "updated"}


# Create a users in db
@app.post(
    "/adduser",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.showuser,
    tags=["Users"],
)
def create_user(req: schemas.user, db: Session = Depends(get_db)):
    new_user = models.user(
        username=req.username, email=req.email, password=Hash.bcrypt(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Getting an User
@app.get(
    "/getuser/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.showuser,
    tags=["Users"],
)
def getuser(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.user = Depends(oauth2.get_current_user),
):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} if not found.",
        )
    return user
