from pydantic import BaseModel

class Response(BaseModel):
  is_error: bool
  message: str
  status: int

def create_error_response(message: str, status: int):
  rp = Response()
  rp.is_error = True
  rp.message = message
  rp.status = status
  return rp

def create_sane_response(message: str, status: int):
  rp = Response()
  rp.is_error = False
  rp.message = message
  rp.status = status
  return rp