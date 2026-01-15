from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime


# users schemas

class UserBase(BaseModel):
    username:str
    email:EmailStr

class UserCreate(UserBase):
    password:str
    is_admin:bool=False
    
class UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(UserBase):
    id:int
    is_admin:bool

    class Config:
        from_attributes=True



# token schema
class Token(BaseModel):
    acces_token:str
    token_type:str

class TokenData(BaseModel):
    username:Optional[str]=None
    # username:str | None=None
    

# movies schemas

class MovieBase(BaseModel):
    title:str
    genre:str
    description:Optional[str]=None
    year:Optional[int]=None
    director:Optional[str]=None
    duration_minutes:Optional[int]=None

class MovieCreate(MovieBase):
    pass



class MovieResponse(MovieBase):
    id: int
    added_by_admin_id: Optional[int] = None  

    class Config:
        orm_mode = True


# watchlist schemas

class WatchListResponse(BaseModel):
    user_id:int
    movies:List[MovieResponse]
    
    class Config:
        from_attributes=True


    