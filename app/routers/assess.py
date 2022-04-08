from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, utils, oauth2
from .. database import get_db
from ..schemas import assess


router = APIRouter(
    prefix='/assessment',
    tags=['Assessments']
)

@router.get("/{id}", response_model=assess.Assessment)
def get_quiz(id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    return quiz

@router.get("/{id}/question", response_model=List[assess.AssessmentQuestion])
def get_quiz_questions(id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == id).all()
    for i, question in enumerate(questions):
        questions[i] = question.__dict__
    return questions

@router.get("/{id}/question/{qid}/answers", response_model=List[assess.AssessmentAnswer])
def get_quiz_question_answers(id: int, qid: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {id} was not found')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    for i, answer in enumerate(answers):
        answers[i] = answer.__dict__
    return answers