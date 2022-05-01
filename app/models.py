from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base


class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    public = Column(Boolean, server_default='FALSE', nullable=False)
    due = Column(TIMESTAMP(timezone=True), server_default=None)
    
    owner = relationship("User")
    

class QuizQuestion(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    
    quiz = relationship("Quiz")
    
class QuizAnswer(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True, nullable=False)
    answer = Column(String, nullable=False)
    correct = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    
    question = relationship("QuizQuestion")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
        
class QuizInstance(Base):
    __tablename__ = 'quizinstances'
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    complete = Column(Boolean, server_default='FALSE', nullable=False)
    
    quiz = relationship("Quiz")
    
class QuizInstanceAnswer(Base):
    __tablename__ = 'quizinstanceanswers'
    
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    instance_id = Column(Integer, ForeignKey("quizinstances.id", ondelete="CASCADE"), nullable=False)
    answer_id = Column(Integer, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    correct = Column(Boolean, server_default='FALSE', nullable=False)
    question_id = Column(Integer, nullable=False)
    
    instance = relationship("QuizInstance")