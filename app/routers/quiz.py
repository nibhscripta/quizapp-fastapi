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
    question = question.dict()
    new_question = models.QuizQuestion(quiz_id=quiz.id, question=question['question'])
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    answers = question['answers']
    for answer in answers:
        new_answer = models.QuizAnswer(question_id=new_question.id, **answer)
        db.add(new_answer)
        db.commit()
    new_question.__dict__['answers'] = answers
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


@router.get("/{id}/question/{qid}")
def get_quiz_question(id: int, qid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    context = {
        'question': question.question, 'id': qid, 'created_at': question.created_at, 'quiz_id': id,
        'answers': []
    }
    for answer in answers:
        answer_dict = {
            'answer': answer.answer, 'correct': answer.correct, 'id': answer.id, 'created_at': answer.created_at, "question_id": qid
        }
        context['answers'].append(answer_dict)
    return context


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


# @router.post("/{id}/question/{qid}/answer", response_model=schemas.QuizAnswerResponse)
# def create_quiz_answer(id: int, qid: int, answer: schemas.QuizAnswer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
#     if not quiz: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
#     question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
#     if not question:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
#     if quiz.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
#     new_answer = models.QuizAnswer(question_id=qid, **answer.dict())
#     db.add(new_answer)
#     db.commit()
#     db.refresh(new_answer)
#     return new_answer


# @router.get("/{id}/question/{qid}/answer/{aid}", response_model=schemas.QuizAnswerResponse)
# def get_quiz_answer(id: int, qid: int, aid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
#     if not quiz: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
#     question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
#     if not question:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
#     if quiz.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
#     answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid).first()
#     if not answer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer with id {aid} was not found')
#     return answer


# @router.delete("/{id}/question/{qid}/answer/{aid}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_quiz_answer(id: int, qid: int, aid: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
#     if not quiz: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
#     question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
#     if not question:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
#     if quiz.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
#     answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
#     if not answer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer with id {aid} was not found')
#     answer.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}/question/{qid}/answer/{aid}", response_model=schemas.QuizAnswerResponse)
# def update_quiz_answer(id: int, qid: int, aid: int, updated_answer: schemas.QuizAnswer, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     quiz = db.query(models.Quiz).filter(models.Quiz.id == id).first()
#     if not quiz: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'quiz with id {id} was not found')
#     question = question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
#     if not question:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'question with id {qid} was not found')
#     if quiz.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this request')
#     answer = db.query(models.QuizAnswer).filter(models.QuizAnswer.id == aid)
#     if not answer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'answer with id {aid} was not found')
#     answer.update(updated_answer.dict(), synchronize_session=False)
#     db.commit()
#     return answer.first()