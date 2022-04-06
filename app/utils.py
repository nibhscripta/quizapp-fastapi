from passlib.context import CryptContext

from . import models


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def questionDict(qid, db):
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == qid).first()
    answers = db.query(models.QuizAnswer).filter(models.QuizAnswer.question_id == qid).all()
    answers_list =[]
    for answer in answers:
        answers_list.append(answer.__dict__)
        
    question.__dict__['answers'] = answers_list
    return question.__dict__