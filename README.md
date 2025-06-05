# JarvisAssistant

JarvisAssistant est un assistant vocal intelligent basé sur FastAPI, Whisper, et Ollama, orchestré via Docker Compose.

## Fonctionnalités principales
- **API LLM** : Interrogation d'un modèle de langage via FastAPI (`api/llm_api.py`)
- **Assistant vocal** : Reconnaissance vocale, transcription et interaction avec le LLM (`voice/jarvis.py`)
- **Prompts personnalisés** : Ajout et gestion de prompts dans `data/prompts.jsonl`
- **Déploiement facile** : Utilisation de Docker Compose pour lancer tous les services

## Structure du projet
- `api/` : Code de l'API FastAPI
- `voice/` : Assistant vocal (reconnaissance, transcription, interaction)
- `data/` : Fichiers de données (prompts)
- `docker-compose.yaml` : Orchestration des services

## Lancement rapide
```sh
docker-compose up --build
```

## Prérequis
- Docker & Docker Compose
- (Optionnel) Python 3.10+ pour développement local

## Auteurs
- Kevin Nicol

---
Pour toute question ou contribution, ouvrez une issue ou une pull request sur le dépôt GitHub.
