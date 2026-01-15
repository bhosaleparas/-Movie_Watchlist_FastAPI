from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth import get_current_user
import crud
from schemas import UserResponse, MovieResponse


router=APIRouter(prefix="/users",tags=["users"])

@router.get('/me',response_model=UserResponse)
def get_user(current_user=Depends(get_current_user)):
    return current_user


@router.get('/watchlist',response_model=List[MovieResponse])
def get_my_watchlist(
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    watchlist=crud.get_watchlist(db,current_user.id)
    return watchlist



# add movie to watchlist
@router.post('/watchlist/{movie_id}',response_model=List[MovieResponse])
def add_movie_to_wathlist(movie_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    movie=crud.get_movie(db,movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="movie not found"
        )
        
    user=crud.add_to_watchlist(db,current_user.id,movie_id)
    return user.watchlist if user else []


# delete movie from watchlist
@router.delete('/watchlist/{movie_id}',response_model=List[MovieResponse])
def remove_movie_from_watchlist(
    movie_id:int,
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    user=crud.remove_from_watchlist(db,current_user.id,movie_id)
    return user.watchlist if user else []


