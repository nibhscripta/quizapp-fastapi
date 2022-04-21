from unittest import result
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import random, string

from app.schemas.quiz import Answer

from .. import models, utils, oauth2
from .. database import get_db
from ..schemas import assess


router = APIRouter(
    prefix='/assessment',
    tags=['Assessments']
)

@router.get("/{id}", response_model=assess.Assessment)
def get_assessment(id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    return quiz

@router.post("/{id}/start", response_model=assess.QuizInstanceResponse)
def start_assessment(id: int, instance: assess.QuizInstance, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    user_id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(12))
    while db.query(models.QuizInstance).filter(models.QuizInstance.user_id == user_id).first():
    new_instanse = models.QuizInstance(user_id=user_id, quiz_id=id, **instance.dict())
    return new_instanse
        


@router.post("/{id}", response_model=List[assess.AssessmentResult])
def post_assessment(id: int, assessment: List[assess.PostAssessment], db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    results = []
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    for question in assessment:
        question_result = {}
        question_query = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == question.question_id).first()
        if not question_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {question.question_id} was not found')
        question_query_question = question_query.question
        answer_query = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == question.answer_id).first()
        if not answer_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer with id {question.answer_id} was not found')
        posted_answer = answer_query.answer
        question_result['question'] = question_query_question
        question_result['posted_answer'] = posted_answer
        if answer_query.correct == True:
            question_result['correct_answer'] = posted_answer
            question_result['correct'] = True
        elif answer_query.correct == False:
            question_result['correct'] = False
            correct_answer =   db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == question.question_id).filter(models.QuizAnswer.correct == True).first().answer
            question_result['correct_answer'] = correct_answer
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        results.append(question_result)
    return results

@router.get("/{id}/question", response_model=List[assess.AssessmentQuestion])
def get_quiz_questions(id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == id).all()
    for i, question in enumerate(questions):
        questions[i] = question.__dict__
    return questions

@router.get("/{id}/question/{qid}/answers", response_model=List[assess.AssessmentAnswer])
def get_quiz_question_answers(id: int, qid: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {id} was not found')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    for i, answer in enumerate(answers):
        answers[i] = answer.__dict__
    return answers

