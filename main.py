from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gptfy import get_response

app = FastAPI()

#class History(BaseModel):
#    question: str
#    answer: str
#DB: List[History] = []
class Question(BaseModel):
    question: str

def process_question(quest: str) -> str:
  return get_response(quest)# <- Blir dyrt å kjøre hver gang

@app.post("/question", tags=["question"])
async def add_question(q: Question) -> str:
    try:
        answer = process_question(q.question)
        #DB.append(History(question=q.question, answer=answer))
        return answer
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.get("/api")
def read_root():
    return "Placeholder for DB"#DB