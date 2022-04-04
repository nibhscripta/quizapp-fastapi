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
def create_quiz(quiz: schemas.Quiz, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_quiz = models.Quiz(owner_id=current_user.id, **quiz.dict())
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
def update_quiz(id:int, updated_quiz:schemas.Quiz, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz_query = db.query(models.Quiz).filter(models.Quiz.id == id)
    quiz = quiz_query.first()
    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} does not exist.')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    quiz_query.update(updated_quiz.dict(), synchronize_session=False)
    db.commit()
    return quiz_query.first()


@router.post("/{id}/question/", response_model=schemas.QuizQuestionResponse)
def create_quiz_question(id: int, question: schemas.QuizQuestion, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if quiz == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} does not exist.')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    new_question = models.QuizQuestion(quiz_id=quiz.id, **question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    print(new_question.id, new_question.question, new_question.created_at, new_question.quiz_id)
    return new_question


@router.get("/{id}/question/", response_model=List[schemas.QuizQuestionResponse])
def get_quiz_questions(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.quiz_id == id).all()
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    return questions


@router.get("/{id}/question/{qid}", response_model=schemas.QuizQuestionResponse)
def get_quiz_question(id: int, qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    return question


@router.delete("/{id}/question/{qid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz_question(id: int, qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid)
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not question.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    question.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}/question/{qid}", response_model=schemas.QuizQuestionResponse)
def update_quiz_question(id: int, qid: int, updated_question: schemas.QuizQuestion , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    question_query = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid)
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not question_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    question_query.update(updated_question.dict(), synchronize_session=False)
    db.commit()
    return question_query.first()