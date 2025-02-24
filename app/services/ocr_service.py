import pytesseract
import os
import cv2
import numpy as np
from PIL import Image
import io
import fitz  # PyMuPDF para extrair texto de PDFs
from pdf2image import convert_from_bytes
import logging

# Configuração do Tesseract OCR
if os.name == "nt":  # Windows
    tesseract_cmd_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Linux (Docker)
    tesseract_cmd_path = "/usr/bin/tesseract"

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
logging.info(f"Caminho do Tesseract usado: {pytesseract.get_tesseract_version()}")

# função pra aplicar pre processamento na imagem
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("L")  # Converte para escala de cinza
        open_cv_image = np.array(image)

        # Ajuste de contraste e brilho
        alpha = 3.0  
        beta = 30  
        adjusted = cv2.convertScaleAbs(open_cv_image, alpha=alpha, beta=beta)

        # Binarização otsu para melhorar contraste (melhorou os resultados no final)
        _, thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # reduzir o ruído
        blurred = cv2.GaussianBlur(thresh, (3, 3), 0)

        return blurred
    except Exception as e:
        logging.error(f"❌ Erro ao pré-processar imagem: {e}")
        return None

# função pra extrair texto de uma imagem usando ocr
def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        processed_image = preprocess_image(image_bytes)
        if processed_image is None:
            return "Erro no pré-processamento da imagem"

        # Aplica OCR na imagem processada
        extracted_text = pytesseract.image_to_string(processed_image, lang="por", config="--psm 6")

        return extracted_text.strip()
    except Exception as e:
        logging.error(f"❌ Erro ao processar imagem no OCR: {e}")
        return "Erro ao processar imagem"
    

# função pra extrair texto de um pdf
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = ""
        with fitz.open("pdf", file_bytes) as doc:
            for page in doc:
                page_text = page.get_text("text")
                if page_text.strip():
                    text += page_text + "\n"

        # Se não encontrou texto no PDF tenta OCR
        return text.strip() if text.strip() else extract_text_from_pdf_with_ocr(file_bytes)
    except Exception as e:
        logging.error(f"❌ Erro ao extrair texto do PDF: {e}")
        return "Erro ao extrair texto do PDF"

#função pra converter pdf pra imagem e aplicar ocr
def extract_text_from_pdf_with_ocr(file_bytes: bytes) -> str:
    try:
        images = convert_from_bytes(file_bytes)  
        if not images:
            return "Erro: Nenhuma imagem gerada para OCR"

        extracted_text = "\n".join(extract_text_from_image(io.BytesIO(img.tobytes())) for img in images)

        return extracted_text.strip()
    except Exception as e:
        logging.error(f"❌ Erro ao processar OCR no PDF: {e}")
        return "Erro ao processar OCR no PDF"
