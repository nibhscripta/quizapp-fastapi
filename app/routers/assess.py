from unittest import result
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.schemas.quiz import Answer

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


@router.post("/{id}", response_model=List[assess.AssessmentResult])
def post_assessment(id: int, assessment: List[assess.PostAssessment], db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    results = []
    for post in assessment:
        question = db.query(models.QuizQuestion).filter(models.QuizQuestion == post.question_id).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {id} was not found')
        answer = db.query(models.QuizAnswer).filter(models.QuizAnswer == post.answer_id).first()
        if not answer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer with id {id} was not found')
        result = {}
        result['question'] = question.question
        result['posted_answer'] = db.query(models.QuizAnswer).filter(models.QuizAnswer == assessment.answer_id).first().answer
        result['correct_answer'] = answer.answer
        if result['posted_answer'] == result['correct_answer']:
            result['correct'] = True
        else: 
            result['correct'] = False
        results.append(result)
    return results
        
        

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

