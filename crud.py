from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from models import User,Movie
from schemas import UserCreate, MovieCreate
import auth


# user crud operation
def get_user_by_username(db:Session,username:str):
    return db.query(User).filter(User.username==username).first()

def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()

def get_user(db:Session,user_id:int):
    return db.query(User).filter(User.id==user_id).first()


def create_user(db:Session,user:UserCreate):
    hashed_password=auth.get_password_hash(user.password)
    db_user=User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# movie crud operation


def get_movie(db:Session,movie_id:int):
    return db.query(Movie).filter(Movie.id==movie_id).first()




def get_movies(db:Session,skip:int=0,limit:int=100):
    return db.query(Movie).offset(skip).limit(limit).all()


def get_movie_by_genre(db:Session,genre:str,skip:int=0,limit:int=100):
    
    return db.query(Movie).filter(func.lower(Movie.genre).contains(genre.lower())).offset(skip).limit(limit).all()



def create_movie(db:Session,movie:MovieCreate,admin_id:int):
    db_movie=Movie(**movie.dict(),added_by_admin_id=admin_id)
    print("from crud",admin_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie



# watchlist operation

def add_to_watchlist(db:Session,user_id:int, movie_id:int):
    user=db.query(User).filter(User.id==user_id).first()
    movie=db.query(Movie).filter(Movie.id==movie_id).first()
    
    if not user or not movie:
        return None

    if movie not in user.watchlist:
        user.watchlist.append(movie)
        db.commit()

    return user


def remove_from_watchlist(db:Session, user_id:int, movie_id:int):
    user=db.query(User).filter(User.id==user_id).first()
    movie=db.query(Movie).filter(Movie.id==movie_id).first()
    
    if not user or not movie:
        return None
    
    if movie  in user.watchlist:
        user.watchlist.remove(movie)
        db.commit()
        
    return user


def get_watchlist(db:Session,user_id:int):
    user=db.query(User).filter(User.id==user_id).first()

    if user:
        return user.watchlist

    return[]   #if not any movie then return empty array


