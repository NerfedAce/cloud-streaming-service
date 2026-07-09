from pydantic import BaseModel

class form(BaseModel):
    user:str
    password:str

class Movie(BaseModel):
    title:str
    length:str
    img:str
    id:int
    url:str
