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

@router.post("/{id}/submit", response_model=List[assess.AssessmentResult])
def submit_assessment(id: int, i: int, u: str, db: Session = Depends(get_db)):
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == i).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != u:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    if instance.complete:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='assessment already submitted')
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()  
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not quiz.public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="this quiz is not public")
    if quiz.due is not None:
        if not db.query(models.Quiz).filter(models.Quiz.id == id).filter(models.Quiz.due < datetime.now()).first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{quiz.title} was due {quiz.due}')
    results = []
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == id).all()
    for question in questions:
        question_result = {}
        question_result['question'] = question.question
        instance_answer = db.query(models.QuizInstanceAnswer).filter(models.QuizInstanceAnswer.instance_id == i, models.QuizInstanceAnswer.question_id == question.id).first()
        if instance_answer:
            question_result['correct'] = instance_answer.correct
            question_result['posted_answer'] = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == instance_answer.answer_id).first().answer
            question_result['correct_answer'] = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == instance_answer.correct_answer_id).first().answer
        else:
            question_result['correct'] = False
            question_result['posted_answer'] = None
            question_result['correct_answer'] = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == question.id, models.QuizAnswer.correct == True).first().answer
        results.append(question_result)
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == i)
    instance.update({'complete':True}, synchronize_session=False)
    db.commit()
    return results
        

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
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == i).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != u:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    return answers

@router.post("/{id}/q/{qid}/i/{i}", response_model=assess.InstanceAnswer)
def post_instance_answer(id: int, qid: int, i: int, u: str, post_answer: assess.InstanceAnswer, db: Session = Depends(get_db)):
    instance_answer = db.query(models.QuizInstanceAnswer).filter(models.QuizInstanceAnswer.instance_id == i, models.QuizInstanceAnswer.question_id == qid).first()
    if instance_answer:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="answer instance exists")
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
    instance = db.query(models.QuizInstance).filter(models.QuizInstance.id == i).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance not found')
    if instance.user_id != u:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
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
    instance_answer = models.QuizInstanceAnswer(question_id=qid, instance_id=i, answer_id=post_answer.answer_id, correct_answer_id=correct_answer_id, correct=correct)
    db.add(instance_answer)
    db.commit()
    return post_answer


@router.put("/{id}/q/{qid}/i/{i}", response_model=assess.InstanceAnswer)
def update_instance_answer(id: int, qid: int, i: int, u: str, post_answer: assess.InstanceAnswer, db: Session = Depends(get_db)):
    instance_answer = db.query(models.QuizInstanceAnswer).filter(models.QuizInstanceAnswer.question_id == qid)
    if not instance_answer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='instance answer not found')
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
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == post_answer.answer_id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='answer does not exist')
    if answer.correct:
        correct = True
    else:
        correct = False
    updated_answer = {
        'answer_id': post_answer.answer_id,
        'correct': correct
    }
    instance_answer.update(updated_answer, synchronize_session=False)
    db.commit()
    return post_answer