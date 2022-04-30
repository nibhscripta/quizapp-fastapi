from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, utils, oauth2
from .. database import get_db
from ..schemas import quiz


router = APIRouter(
    prefix='/ans',
    tags=['Answers']
)


@router.get("", response_model=List[quiz.AnswerResponse])
def get_answers(qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question.quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    return answers


@router.post("", response_model=quiz.AnswerResponse)
def create_answer(qid: int, answer: quiz.Answer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    answer = answer.dict()
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question.quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()        
    if len(answers) > 3:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='question has four answers')
    true_answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid, models.QuizAnswer.correct == True).all()
    if len(answers) > 2:
        if not true_answers:
            answer['correct'] = True
    new_answer = models.QuizAnswer(question_id=qid, **answer)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@router.delete("/{aid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz_answer(aid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
    if not answer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == answer.first().question_id).first()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question.quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answer.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{aid}", response_model=quiz.AnswerResponse)
def update_quiz_answer(aid: int, updated_answer: quiz.Answer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_answer =  updated_answer.dict()
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
    if not answer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == answer.first().question_id).first()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == question.quiz_id).first()
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answer.update(updated_answer, synchronize_session=False)
    db.commit()
    return answer.first()