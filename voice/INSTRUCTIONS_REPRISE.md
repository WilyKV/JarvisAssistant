<<<<<<< HEAD
# ...existing code from your workspace...
=======
# Instructions de reprise pour JarvisAssistant (voice)

## Fonctionnement actuel

- Écoute continue du micro, découpage en segments d'1 seconde.
- Détection de la voix sur chaque segment avec webrtcvad (aggressiveness=2).
- Tant qu'il y a de la voix, les segments sont cumulés.
- Si 5 secondes consécutives sans voix sont détectées, on considère que la prise de parole est terminée.
- Tous les segments sont fusionnés en un seul fichier audio.
- Le fichier fusionné est transcrit avec Whisper (modèle local).
- Le texte transcrit est envoyé à l'API LLM locale (http://localhost:8200/query).
- Après la réponse, tous les fichiers audio temporaires sont supprimés.
- Le script recommence automatiquement une nouvelle session d'écoute.

## Points techniques

- Utilisation de SpeechRecognition pour l'enregistrement audio.
- Utilisation de webrtcvad pour la détection de la voix (Voice Activity Detection).
- Utilisation de Whisper pour la transcription audio -> texte.
- Utilisation de requests pour l'appel à l'API LLM.
- Les fichiers audio temporaires sont stockés dans le dossier `audio_tmp/`.
- Les dépendances principales sont installées dans le Dockerfile (pyaudio, numpy, openai-whisper, requests, SpeechRecognition, webrtcvad).

## Améliorations/Problèmes à traiter la prochaine fois

- Vérifier la robustesse de la détection de voix (ajuster aggressiveness ou segment_duration si besoin).
- Améliorer la gestion des coupures ou des faux positifs/negatifs de la VAD.
- Ajouter éventuellement une interface utilisateur ou des logs plus détaillés.
- Tester sur différentes machines/environnements (Windows, Docker, etc).
- Ajouter des tests unitaires ou d'intégration si besoin.

## Commandes utiles

- Installation locale de webrtcvad :
  ```
  py -m pip install webrtcvad
  ```
- Reconstruction de l'image Docker :
  ```
  docker build -f .docker/Dockerfile-voice -t jarvis-voice .
  ```

---

**Reprendre ici pour toute évolution ou debug !**

>>>>>>> e467a78 (chore: synchronisation complète du dossier local avec main (README global, suppression README voice, suppression .wav, etc.))
