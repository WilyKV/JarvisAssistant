import speech_recognition as sr
import pyaudio
import whisper
import requests
import numpy as np
import warnings
import io
import tempfile
import os
import uuid
import wave
import time
import traceback
import collections
import webrtcvad

AUDIO_TMP_DIR = os.path.join(os.path.dirname(__file__), 'audio_tmp')
os.makedirs(AUDIO_TMP_DIR, exist_ok=True)

warnings.filterwarnings("ignore")

recognizer = sr.Recognizer()
micro = sr.Microphone()
model = whisper.load_model("base")

def is_voice(audio_data, sample_rate=16000, aggressiveness=2):
    vad = webrtcvad.Vad(aggressiveness)
    # webrtcvad attend du 16kHz mono 16bit PCM
    # On tronque à un multiple de 30ms (480 échantillons à 16kHz)
    frame_ms = 30
    frame_len = int(sample_rate * frame_ms / 1000) * 2  # 2 bytes/sample
    voiced = False
    for i in range(0, len(audio_data) - frame_len + 1, frame_len):
        frame = audio_data[i:i+frame_len]
        if len(frame) < frame_len:
            continue
        if vad.is_speech(frame, sample_rate):
            voiced = True
            break
    return voiced

def merge_wav_files(wav_files, output_path):
    # Fusionne plusieurs fichiers WAV mono en un seul
    import wave
    data = []
    params = None
    for fname in wav_files:
        with wave.open(fname, 'rb') as wf:
            if params is None:
                params = wf.getparams()
            data.append(wf.readframes(wf.getnframes()))
    with wave.open(output_path, 'wb') as wf:
        wf.setparams(params)
        for d in data:
            wf.writeframes(d)

print("Parlez, l'assistant va transcrire et répondre...")

segment_duration = 1  # secondes
silence_limit = 5     # secondes

while True:
    audio_segments = []
    silence_count = 0
    print("En écoute continue...")
    with micro as source:
        recognizer.adjust_for_ambient_noise(source)
        listening = True
        while listening:
            audio = recognizer.record(source, duration=segment_duration)
            raw_data = audio.get_raw_data()
            tmpfile_path = os.path.join(AUDIO_TMP_DIR, f"audio_{uuid.uuid4().hex}.wav")
            # Sauvegarde du segment
            sample_width = getattr(audio, 'sample_width', 2)
            sample_rate = getattr(audio, 'sample_rate', 16000)
            with wave.open(tmpfile_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(sample_width)
                wf.setframerate(sample_rate)
                wf.writeframes(raw_data)
            audio_segments.append(tmpfile_path)
            # Détection de la voix avec webrtcvad
            if is_voice(raw_data, sample_rate=sample_rate):
                silence_count = 0
            else:
                silence_count += segment_duration
            if silence_count >= silence_limit:
                print("Silence détecté, transcription...")
                listening = False
    # Fusion des segments
    merged_path = os.path.join(AUDIO_TMP_DIR, f"merged_{uuid.uuid4().hex}.wav")
    merge_wav_files(audio_segments, merged_path)
    try:
        result = model.transcribe(merged_path, language='fr')
        commande = result["text"].strip()
        print(f"Commande transcrite : {commande}")
        if commande:
            try:
                r = requests.post("http://localhost:8200/query", json={"prompt": commande})
                print("Réponse de l'IA :", r.json().get("response", r.text))
            except Exception as e:
                print("Erreur lors de l'appel à l'API LLM :", e)
        else:
            print("Aucune commande détectée.")
    except Exception as e:
        print(f"Erreur : {e}")
        traceback.print_exc()
    finally:
        # Suppression des segments et du fichier fusionné
        for f in audio_segments + [merged_path]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception as ex:
                    print(f"Erreur suppression fichier temporaire : {ex}")
