from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import User, Rating, Movie
from ..schemas import UserOut, RatingIn, RatingOut

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}/ratings", response_model=List[RatingOut])
def get_ratings(user_id: int, db: Session = Depends(get_db)):
    return db.query(Rating).filter(Rating.user_id == user_id).all()

@router.post("/{user_id}/ratings", response_model=RatingOut)
def upsert_rating(user_id: int, payload: RatingIn, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    movie = db.query(Movie).get(payload.movie_id)
    if not user or not movie:
        raise HTTPException(status_code=404, detail="User or movie not found")
    r = db.query(Rating).filter(Rating.user_id == user_id, Rating.movie_id == payload.movie_id).one_or_none()
    if r:
        r.rating = payload.rating
    else:
        r = Rating(user_id=user_id, movie_id=payload.movie_id, rating=payload.rating)
        db.add(r)
    db.commit()
    db.refresh(r)
    return r
