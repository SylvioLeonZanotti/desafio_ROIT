# Usa a imagem base do Python
FROM python:3.10

# Instala dependências do sistema (incluindo Tesseract OCR e OpenCV)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    python3-opencv \
    poppler-utils

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando padrão ao rodar o container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
