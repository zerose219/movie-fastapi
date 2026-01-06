from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import Movie
from ..schemas import MovieOut

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("", response_model=List[MovieOut])
def list_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies
