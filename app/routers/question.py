from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, utils, oauth2
from .. database import get_db
from ..schemas import quiz


router = APIRouter(
    prefix='/ques',
    tags=['Questions']
)

@router.post("", response_model=quiz.QuizQuestionResponse)
def create_quiz_question(quiz_id: str, question: quiz.QuizQuestion, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    new_question = models.QuizQuestion(quiz_id=quiz_id, **question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@router.get("", response_model=List[quiz.QuizQuestionResponse])
def get_quiz_questions(quiz_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == quiz_id).all()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    return questions


@router.delete("/{qid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz_question(qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid)
    if not question.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question.first().quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    question.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{qid}", response_model=quiz.QuizQuestionResponse)
def update_quiz_question(qid: int, updated_question: quiz.QuizQuestion, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    question_query = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid)
    if not question_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question_query.first().quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not unauthorized')
    question_query.update(updated_question.dict(), synchronize_session=False)
    db.commit()
    return question_query.first()