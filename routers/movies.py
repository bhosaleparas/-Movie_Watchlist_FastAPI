from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import crud
from schemas import MovieResponse



router=APIRouter(prefix="/movies",tags=["movies"])


# getting all movies
@router.get('/',response_model=List[MovieResponse])
def get_movies(
    skip:int=0,limit:int=100,
    db:Session=Depends(get_db)
):
    
    return crud.get_movies(db,skip=skip,limit=limit)

   
   
# search for movie

@router.get("/search",response_model=List[MovieResponse])
def search_movies_by_degree(
    genre:str=Query(...,description="search movie by genre"),
    skip:int=0,
    limit:int=100,
    db:Session=Depends(get_db)
):
    return crud.get_movie_by_genre(db,genre=genre,skip=skip,limit=limit) 


@router.get('/{movie_id}',response_model=MovieResponse)
def get_movie(
    movie_id:int,
    db:Session=Depends(get_db)

):
    movie=crud.get_movie(db,movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404,detail="movie not found")
    return movie