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
    prefix='/a',
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
        user_id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(12))
    new_instance = models.QuizInstance(user_id=user_id, quiz_id=id, **instance.dict())
    db.add(new_instance)
    db.commit()
    db.refresh(new_instance)
    return new_instance
        

@router.get("/{id}/q", response_model=List[assess.AssessmentQuestion])
def get_quiz_questions(id: int, i: int, u: str, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == i).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != u:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == id).all()
    return questions

@router.get("/{id}/q/{qid}/ans", response_model=List[assess.AssessmentAnswer])
def get_quiz_question_answers(id: int, qid: int, i: int, u: str, db: Session = Depends(get_db)):
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

@router.post("/{id}/question/{qid}/instance", response_model=assess.InstanceAnswer)
def post_instance_answer(id: int, qid: int, post_answer: assess.InstanceAnswer, db: Session = Depends(get_db)):
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
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == post_answer.instance_id).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != post_answer.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this instance is not yours")
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == post_answer.answer_id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='answer does not exist')
    if answer.correct:
        correct_answer_id = post_answer.answer_id
        correct = True
    else:
        correct_answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid, models.QuizAnswer.correct == True).first()
        correct_answer_id = correct_answer.id
        correct = False
    instance_answer = models.QuizInstanceAnswer(instance_id=post_answer.instance_id, answer_id=post_answer.answer_id, correct_answer_id=correct_answer_id, correct=correct)
    db.add(instance_answer)
    db.commit()
    return post_answer


@router.put("/{id}/question/{qid}/instance", response_model=assess.InstanceAnswer)
def update_instance_answer(id: int, qid: int, post_answer: assess.InstanceAnswer, db: Session = Depends(get_db)):
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
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == post_answer.instance_id).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != post_answer.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this instance is not yours")
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == post_answer.answer_id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='answer does not exist')
    if answer.correct:
        correct_answer_id = post_answer.answer_id
        correct = True
    else:
        correct_answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid, models.QuizAnswer.correct == True).first()
        correct_answer_id = correct_answer.id
        correct = False
    instance_answer = db.query(models.QuizInstanceAnswer).filter(models.QuizInstanceAnswer.instance_id == post_answer.instance_id)
    if not instance_answer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance does not exist')
    instance_answer.update(post_answer.dict(), correct_answer_id, correct, synchronize_session=False)
    db.commit()
    return post_answer