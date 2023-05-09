import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gptfy import get_response

app = FastAPI()

class Question(BaseModel):
    question: str
    history: list

class Password(BaseModel):
    password: str

def process_question(quest: str, hist: list) -> str:
  return get_response(quest, hist)

@app.post("/question", tags=['question'])
async def add_question(q: Question) -> str:
    try:
        answer = process_question(q.question, q.history)
        return answer
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/password", tags=["password"])
async def check_passwrod(p: Password) -> bool:
    try:
        given_password =p.password
        password = os.getenv('PASSWORD')
        return (given_password==password)
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))