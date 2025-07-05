from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil
from PyPDF2 import PdfReader, PdfWriter
from uuid import uuid4

router = APIRouter()

TEMP_DIR = "temp_pdfs"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/dividir-pdf")
async def dividir_pdf(file: UploadFile = File(...)):
    input_path = f"{TEMP_DIR}/{uuid4().hex}_{file.filename}"

    # Guardar PDF temporal
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        page_urls = []

        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            page_filename = f"{input_path}_page_{i+1}.pdf"
            with open(page_filename, "wb") as f:
                writer.write(f)

            page_urls.append(f"/archivos/{os.path.basename(page_filename)}")

        return {"paginas": total_pages, "archivos": page_urls}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
