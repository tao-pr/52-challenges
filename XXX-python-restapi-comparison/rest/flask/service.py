from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
  return {"api": "fastapi"}

@app.post("/post/{id}")
def post():
  pass # TAOTODO