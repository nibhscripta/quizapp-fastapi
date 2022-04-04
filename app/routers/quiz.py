from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/quiz',
    tags=['Quizzes']
)


@router.get("/", response_model=List[schemas.QuizResponse])
def get_quizzes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quizzes = db.query(models.Quiz).filter(models.Quiz.owner_id == current_user.id).all()
    return quizzes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.QuizResponse)
def create_quiz(post: schemas.QuizBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_quiz = models.Quiz(owner_id=current_user.id, **post.dict())
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.get("/{id}", response_model=schemas.QuizResponse)
def get_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id, models.Quiz.owner_id == current_user.id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    return quiz


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id)
    if quiz.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} does not exist.')
    if quiz.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    quiz.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.QuizResponse)
def update_quiz(id:int, updated_post:schemas.QuizBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz_query = db.query(models.Quiz).filter(models.Quiz.id == id)
    quiz = quiz_query.first()
    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} does not exist.')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    quiz_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return quiz_query.first()