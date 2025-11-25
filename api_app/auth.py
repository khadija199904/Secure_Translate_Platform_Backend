from utils import pwd_context , SECRET_KEY,ALGORITHM 
from fastapi import Header ,HTTPException
from jose import jwt



# veification de password hashing
def verify_password_hash(normal_password, hashed_password):
        return pwd_context.verify(normal_password, hashed_password)



# verificatin de token cree en login
def verify_token(token : str = Header()):
  try:
      token_decoded = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
      return token_decoded
  except :
      #  GESTION TOKEN MANQUANT
      raise HTTPException(status_code=401,detail="Token d'authentification manquant")
  
 