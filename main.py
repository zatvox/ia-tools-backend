from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import librosa
import soundfile as sf
import noisereduce as nr
from uuid import uuid4

app = FastAPI()

# 🛡️ CORS CONFIGURACIÓN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a ["http://localhost:5173"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/limpiar-audio")
async def limpiar_audio(file: UploadFile = File(...)):
    input_filename = f"{UPLOAD_DIR}/{uuid4().hex}_{file.filename}"
    output_filename = input_filename.replace(".", "_cleaned.")

    # Guardar archivo recibido
    with open(input_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Cargar el audio
        y, sr = librosa.load(input_filename, sr=None)
        reduced = nr.reduce_noise(y=y, sr=sr)
        sf.write(output_filename, reduced, sr)

        return FileResponse(
            output_filename,
            media_type="audio/wav",
            filename="audio-limpio.wav"
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(input_filename):
            os.remove(input_filename)
