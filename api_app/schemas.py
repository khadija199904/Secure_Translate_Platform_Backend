from pydantic import BaseModel
from typing import Literal




class UserRegister(BaseModel):
    username : str
    email : str 
    password : str
     

class UserResponse(BaseModel):
    username: str
    email: str
    password_hash :str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username : str 
    password :str


# schema pour le texte reçu dans la requête POST /translate.
class TextInput (BaseModel):
    text : str


class TranslateOutput(BaseModel):
    translation_text : str