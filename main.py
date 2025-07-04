from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
import librosa
import soundfile as sf
import noisereduce as nr
from uuid import uuid4

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/limpiar-audio")
async def limpiar_audio(file: UploadFile = File(...)):
    file_id = uuid4().hex
    input_filename = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    output_filename = f"{UPLOAD_DIR}/{file_id}_cleaned.wav"  # ← Siempre en WAV

    # Guardar archivo recibido
    with open(input_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Cargar el audio con librosa
        y, sr = librosa.load(input_filename, sr=None)

        # Reducir ruido
        reduced = nr.reduce_noise(y=y, sr=sr)

        # Guardar resultado como .wav
        sf.write(output_filename, reduced, sr)

        return FileResponse(
            output_filename,
            media_type="audio/wav",
            filename="audio-limpio.wav"
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Limpia el archivo subido
        if os.path.exists(input_filename):
            os.remove(input_filename)

