from fastapi import FastAPI
from  api_app.database import Base,engine,SessionLocal






app = FastAPI(title="Plateforme de Traduction Sécurisée API")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close



# @app.post('/login')
