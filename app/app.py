from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .routers import user, auth, quiz, assess, question, answer


origins = [
           "*"
           ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(assess.router)
app.include_router(question.router)
app.include_router(answer.router)
