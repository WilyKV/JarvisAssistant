from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
import json

app = FastAPI()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
PROMPTS_FILE = os.path.join(os.path.dirname(__file__), '../data/prompts.jsonl')

@app.post("/query")
async def query_llm(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Corps JSON invalide.")
    prompt = data.get('prompt')
    if not prompt:
        raise HTTPException(status_code=422, detail="Champ 'prompt' manquant.")
    try:
        response = requests.post(OLLAMA_URL, json={
            'model': 'phi3',
            'prompt': prompt,
            'system': "Tu es un assistant IA. Réponds toujours en français, même si la question est posée dans une autre langue.",
            'stream': False
        })
        response.raise_for_status()
        # Gestion d'une réponse multi-JSON (JSONL)
        lines = response.text.strip().splitlines()
        results = []
        for line in lines:
            try:
                results.append(json.loads(line))
            except Exception:
                continue
        if not results:
            raise HTTPException(status_code=500, detail=f"Réponse Ollama non valide: {response.text}")
        return results[-1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Ollama: {str(e)}")

@app.post("/add-prompt")
async def add_prompt(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Corps JSON invalide.")
    prompt = data.get('prompt')
    completion = data.get('completion')
    if not prompt or not completion:
        raise HTTPException(status_code=422, detail="Champs 'prompt' et 'completion' requis.")
    entry = {"prompt": prompt, "completion": completion}
    try:
        with open(PROMPTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return {"status": "ok", "message": "Prompt ajouté."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur écriture fichier: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok"}
