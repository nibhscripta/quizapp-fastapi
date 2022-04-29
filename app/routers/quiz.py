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





@router.get("/{id}/ques/{qid}/an", response_model=List[quiz.AnswerResponse])
def get_answers(id: int, qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if not quiz: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    return answers


@router.post("/{id}/ques/{qid}/an", response_model=quiz.AnswerResponse)
def create_answer(id: int, qid: int, answer: quiz.Answer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    answer = answer.dict()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if not quiz: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
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


@router.delete("/{id}/ques/{qid}/an/{aid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz_answer(id: int, qid: int, aid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if not quiz: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer not found')
    answer.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}/ques/{qid}/an/{aid}", response_model=quiz.AnswerResponse)
def update_quiz_answer(id: int, qid: int, aid: int, updated_answer: quiz.Answer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_answer =  updated_answer.dict()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if not quiz: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz not found')
    question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorized')
    answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
    if not answer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer not found')
    answer.update(updated_answer, synchronize_session=False)
    db.commit()
    return answer.first()