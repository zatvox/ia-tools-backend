from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import replicate
import os

router = APIRouter()

# ✅ Define el modelo de entrada
class PromptRequest(BaseModel):
    prompt: str

# ✅ Cargar token de Replicate (puedes usar variables de entorno o ponerlo directo)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN") 

if not REPLICATE_API_TOKEN:
    raise RuntimeError("Falta configurar REPLICATE_API_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# ✅ Ruta para generar imagen
@router.post("/generar-imagen")
async def generar_imagen(request: PromptRequest):
    try:
        output = replicate_client.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
        input={"prompt": request.prompt}
        )
        if isinstance(output, list) and output:
            return {"image_url": output[0]}
        raise HTTPException(status_code=500, detail="No se pudo generar imagen")
    except Exception as e:
        print("❌ ERROR AL GENERAR IMAGEN:", str(e))  # 👈🏼 Esta línea es clave
        raise HTTPException(status_code=500, detail="Error interno al generar imagen")
