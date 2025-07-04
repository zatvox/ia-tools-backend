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
    allow_origins=["*"],  # Puedes cambiarlo por ["http://localhost:5173"] si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/limpiar-audio")
async def limpiar_audio(file: UploadFile = File(...)):
    input_filename = f"{UPLOAD_DIR}/{uuid4().hex}_{file.filename}"
    output_filename = os.path.splitext(input_filename)[0] + "_cleaned.wav"  # ✅ Nombre correcto

    # Guardar archivo recibido
    with open(input_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Cargar y limpiar audio
        y, sr = librosa.load(input_filename, sr=None)
        reduced = nr.reduce_noise(y=y, sr=sr)

        # Guardar audio limpio en formato WAV compatible
        sf.write(output_filename, reduced, sr, subtype="PCM_16")  # ✅ Códec compatible con navegador

        return FileResponse(
            output_filename,
            media_type="audio/wav",
            filename="audio-limpio.wav"
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Eliminar archivo original (pero no el limpio)
        if os.path.exists(input_filename):
            os.remove(input_filename)
