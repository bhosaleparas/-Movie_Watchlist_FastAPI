from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_admin
import crud
from schemas import MovieCreate, MovieResponse

router=APIRouter(prefix="/admin",tags=["admin"])


# create a new movie
@router.post("/movies",response_model=MovieResponse)
def create_movie(movie:MovieCreate,current_user=Depends(get_current_admin),db:Session=Depends(get_db)):
    print("from crud",current_user.id)
    return crud.create_movie(db,movie,admin_id=current_user.id)


# get all movies
@router.get('/movies',response_model=List[MovieResponse])
def get_all_moives(
    skip:int=0,limit:int=100,
    current_user=Depends(get_current_admin),
    db:Session=Depends(get_db)
):
    movies=crud.get_movies(db,skip=skip,limit=limit)
    return movies


