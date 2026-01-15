from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between users and movies (watchlist)
user_movies = Table(
    'user_movies',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    # Relationship to watchlist
    watchlist = relationship("Movie", secondary=user_movies, back_populates="users")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    description = Column(String)
    year = Column(Integer)
    director = Column(String)
    duration_minutes = Column(Integer)
    added_by_admin_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship to users who added this to watchlist
    users = relationship("User", secondary=user_movies, back_populates="watchlist")
    added_by = relationship("User")