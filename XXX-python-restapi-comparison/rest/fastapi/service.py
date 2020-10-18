from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from rest.flask.model.data import *

app = FastAPI()

@app.get("/")
def root():
  return {"api": "fastapi"}

@app.post("/post/{id}")
def post():
  # Parse input as JSON
  return create_error_response("NOT IMPLEMENTED", 500)

@app.post("/post/upload/{id}")
async def upload(cate: str = "receipt"):
  return create_error_response("NOT IMPLEMENTED", 500)