from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, utils, oauth2
from .. database import get_db
from ..schemas import quiz


router = APIRouter(
    prefix='/q',
    tags=['Quizzes']
)


@router.get("/", response_model=List[quiz.QuizResponse])
def get_quizzes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), p: int = 0):
    quizzes = db.query(models.Quiz).filter(models.Quiz.owner_id == current_user.id).limit(20).offset(p).all()
    return quizzes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=quiz.QuizResponse)
def create_quiz(quiz: quiz.Quiz, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_quiz = models.Quiz(owner_id=current_user.id, **quiz.dict())
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.get("/{id}", response_model=quiz.QuizResponse)
def get_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id, models.Quiz.owner_id == current_user.id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    return quiz


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id)
    if quiz.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    if quiz.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    quiz.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=quiz.QuizResponse)
def update_quiz(id:int, updated_quiz:quiz.Quiz, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz_query = db.query(models.Quiz).filter(models.Quiz.id == id)
    quiz = quiz_query.first()
    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    quiz_query.update(updated_quiz.dict(), synchronize_session=False)
    db.commit()
    return quiz_query.first()
