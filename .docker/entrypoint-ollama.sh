#!/bin/bash
set -e

# Démarre le serveur Ollama en arrière-plan
ollama serve &

# Attendre que le serveur soit prêt
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

# Télécharger le modèle phi2 (ou phi3 si tu préfères)
ollama pull phi3

# Garde le serveur en avant-plan
wait -n
