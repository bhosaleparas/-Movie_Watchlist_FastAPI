from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

from database import engine, get_db, Base
from models import User, Movie


from database import engine,get_db,Base
from models import User, Movie
from auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash
)

from schemas import UserCreate,UserResponse, Token

import crud
from routers import users, admin, movies


# create tables on db
Base.metadata.create_all(bind=engine)


app=FastAPI(
    title="Movie Watchlist API",
    description="movie watchlist with user and admin roles",
    version="1.0.0"
)

print("App loading.....")
# include routers of user,movie and admin

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(admin.router)




# reistration
@app.post('/register',response_model=UserResponse)
def regisetr(user:UserCreate,db:Session=Depends(get_db)):
    
    # check for user
    db_user=crud.get_user_by_username(db,username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exists"
        )
    
    db_email=crud.get_user_by_email(db,email=user.email)
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already exists"
        )
    
    # manual setting of admin is avilable
    if user.is_admin:
        user.is_admin=False
        
    return crud.create_user(db=db,user=user)


# login

@app.post('/login',response_model=Token)
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not  user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    acces_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(data={"sub":user.username},expires_delta=acces_token_expires)

    return {"acces_token":access_token , "token_type": "Bearer"}

    

@app.get("/")
def root():
    return{
            "message":"Welcome to Movie watchlist Api",
            "docs":"/docs",
            "redocs":"/redocs",
            "advice":"use /docs "
        }
        
        
    