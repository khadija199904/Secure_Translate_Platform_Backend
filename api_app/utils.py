
from fastapi import HTTPException
from schemas import UserRegister
from dotenv import load_dotenv
import os
from jose import jwt 
from passlib.context import CryptContext
from models import USER

load_dotenv
 

 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"




# On configure l'outil qui va crypter les mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# creation neveau user

def create_user (user_data : UserRegister):
    hashed_password = get_password_hash(user_data.password)
    new_user = USER(email=user_data.email,username=user_data.username,password_hash=hashed_password)
    return new_user


# creation token pour nauveau utilisateur

def create_token (user : UserRegister,) :
   
    payload = { "Username" : user.username}
    token = jwt.encode(payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token





if __name__ == "__main__":
  fake_user = UserRegister(username="testuser", email="test@example.com", password="123456")

  user1 =create_user(fake_user)
  print(user1.email)
   