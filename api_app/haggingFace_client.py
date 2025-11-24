import os
import requests
from dotenv import load_dotenv


load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


if not HF_API_TOKEN:
    raise ValueError("La clé d'API Hugging Face n'est pas définie. Veuillez la mettre dans le fichier .env")



# api url for translation FR to EN
FR_EN_URL = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-fr-en"

# api url for translation EN to FR
EN_FR_URL ="https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-fr"



headers = {"Authorization": f"Bearer {HF_API_TOKEN}",}


def translate_text(text,API_URL):
    if not text :
        return None
    payload = {"inputs": text}

    try:
        hf_response = requests.post(API_URL , headers=headers,json=payload,timeout=30)
        hf_response.raise_for_status() 
        
        return
       
    except requests.exceptions.Timeout :
         return {"error": "Le délai d'attente a expiré (Timeout)."}

    if hf_response.status_code == 503:
            return {"error": "service Hugging Face indisponible"}
    