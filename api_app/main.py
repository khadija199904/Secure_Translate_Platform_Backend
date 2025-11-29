from fastapi import FastAPI,HTTPException ,Depends
from sqlalchemy.orm import Session
from database import Base,engine,SessionLocal
from schemas import TextInput , UserRegister ,UserLogin,UserResponse,TranslateOutput
from haggingFace_client import translate_text
from utils import create_user,create_token
from models import USER
from typing import Literal
from auth import verify_token,verify_password_hash
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Plateforme de Traduction Sécurisée API")


# --- Configuration CORS pour autoriser le frontend ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()





# Endpoint Register protégée
@app.post('/register')
async def singup(user : UserRegister, db: Session = Depends(get_db) ) :
   
   existing_user = db.query(USER).filter(USER.email == user.email ).first()
   if existing_user:
         raise HTTPException(status_code=400,detail="Email Déja existe")
   
   new_user = create_user(user)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return  {"message": "Compte créé avec succès", "username": new_user.username, "email": new_user.email}
    

  



# Endpoint login protégée

@app.post("/login") 
async def login(user : UserLogin,db: Session = Depends(get_db)):
     
     user_data = db.query(USER).filter(USER.username == user.username ).first()
     # Vérification username et password
     if not user_data or not verify_password_hash(user.password, user_data.password_hash):
        raise HTTPException(status_code=401,detail="Access Failed (Incorrect username or password)")
     
     token = create_token(user_data) 
     return {"access_token": token }
         

# Endpoint de translation protégée
@app.post('/translate',response_model=TranslateOutput) 
async def translate(request: TextInput,translation_sens: Literal["fr-en", "en-fr"],new_user : str = Depends(verify_token)) :

    API_URL = f"https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-{translation_sens}"
    text = request.text
    
    translated_text =  translate_text(text,API_URL)
   
    
    return TranslateOutput(translation_text=translated_text)

    
#   # Endpoint de translation sans protection 
# @app.post('/translate_test') 
# async def translate(request: TextInput,translation_sens: Literal["fr-en", "en-fr"]) :

#     if translation_sens not in ["fr-en", "en-fr"]:
#         raise HTTPException(status_code=400, detail="Mauvais format d’entree(Le sens de traduction doit être 'fr-en' ou 'en-fr').")
    
#     API_URL = f"https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-{translation_sens}"
#     text = request.text
    
#     translated_text =  translate_text(text,API_URL)

#     return TranslateOutput(translation_text=translated_text)