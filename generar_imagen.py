from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import replicate
import os

router = APIRouter()

# ✅ Cargar token de Replicate desde variable de entorno
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    raise RuntimeError("Falta configurar REPLICATE_API_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generar-imagen")
async def generar_imagen(request: PromptRequest):
    try:
        output = replicate_client.run(
            "stability-ai/stable-diffusion@db21e45c",  # modelo gratuito
            input={"prompt": request.prompt}
        )
        if isinstance(output, list) and output:
            return {"image_url": output[0]}
        raise HTTPException(status_code=500, detail="No se pudo generar la imagen")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ ERROR AL GENERAR IMAGEN: {str(e)}")

