import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


if not HF_API_TOKEN:
    raise ValueError("La clé d'API Hugging Face n'est pas définie. Veuillez la mettre dans le fichier .env")


headers = {"Authorization": f"Bearer {HF_API_TOKEN}",}


def translate_text(text,API_URL):
    if not text :
        return None
    payload = {"inputs": text}

    try:
        hf_response = requests.post(API_URL , headers=headers,json=payload,timeout=30)
        hf_response.raise_for_status() 
        result = hf_response.json()
        translated_text = result[0]['translation_text']
        return translated_text
       
    except requests.exceptions.Timeout :
         raise HTTPException(status_code=504, detail="Hugging Face ne répond pas (Timeout).")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Erreur de connexion au serveur HF.")
    except (ValueError, KeyError, IndexError, TypeError) as e:
        # print erreur dans le console
        print(f"Erreur de format : {e}") 
       
        raise HTTPException(status_code=500, detail="Réponse mal formée reçue de l'API.")
