from fastapi import APIRouter, HTTPException
import logging
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf

logging.basicConfig(level=logging.INFO)
router = APIRouter()

# função pra extrair o texto dos docs
@router.post("/extract_text")
async def extract_text_from_document(file_type: str, file_bytes: bytes): 

    try:
        if file_type == "image":
            extracted_text = extract_text_from_image(file_bytes)
        elif file_type == "pdf":
            extracted_text = extract_text_from_pdf(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")

        if not extracted_text:
            raise HTTPException(status_code=400, detail="Falha ao extrair texto.")

        logging.info(f"✅ Texto extraído ({file_type}): {extracted_text[:500]}")
        return {"texto_extraido": extracted_text}

    except Exception as e:
        logging.error(f"❌ Erro na extração de texto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na extração de texto: {str(e)}")
