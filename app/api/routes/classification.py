from fastapi import APIRouter, File, UploadFile, HTTPException
import json
import logging
import gzip
import io
from typing import List
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf
from app.services.mistral_service import mistral_service
from app.services.storage_service import salvar_resultados

logging.basicConfig(level=logging.INFO)
router = APIRouter()

#funnção pra descompactar arquigo .gz e converter para json
def decode_pb_gz(file_bytes: bytes):

    try:
        with gzip.GzipFile(fileobj=io.BytesIO(file_bytes), mode="rb") as gz_file:
            pb_data = gz_file.read()  

        try:
            json_data = json.loads(pb_data.decode("utf-8"))
            return json.dumps(json_data)[:3000] #tentativa de limitar em 3000 caracteres pra evitar erro
        except:
            return pb_data.hex()[:3000]  #se não for JSON, retorna HEX truncado

    except Exception as e:
        logging.error(f"❌ Erro ao processar .pb.gz: {e}")
        return None

#função pra enviar os arquivos e classificar usanod mistral 7b
@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...), nome_arquivo: str = "resultados.json"):
    resultados = []

    for file in files:
        try:
            contents = await file.read()
            logging.info(f"📌 Recebendo arquivo: {file.filename} ({len(contents)} bytes)")

            if not contents:
                raise HTTPException(status_code=400, detail=f"Arquivo {file.filename} está vazio.")

            extracted_text = None

            # se for imagem usa OCR
            if file.content_type.startswith("image/"):
                extracted_text = extract_text_from_image(contents)

            # se for pdf usa PyMuPDF ou OCR
            elif file.content_type == "application/pdf":
                extracted_text = extract_text_from_pdf(contents)

            # se for json usa o conteudo do arquivo
            elif file.content_type == "application/json":
                document = json.loads(contents)
                extracted_text = json.dumps(document, ensure_ascii=False)

            # se for um .pb.gz tenta descompactar e processar
            elif file.filename.endswith(".pb.gz"):
                extracted_text = decode_pb_gz(contents)

            else:
                raise HTTPException(status_code=400, detail=f"arquivo {file.filename} não suportado.")

            if not extracted_text:
                raise HTTPException(status_code=400, detail=f"falha ao extrair texto do documento {file.filename}.")

            extracted_text = extracted_text[:3000]

            # prompt de classificação do mistral
            prompt = f"""
            Analise o seguinte texto extraído de um documento e forneça:
            - O CNPJ, caso presente
            - O código de barras, caso presente
            - A classificação do documento (boleto, nota fiscal ou comprovante)

            Texto extraído (limitado a 3000 caracteres):
            \"\"\"{extracted_text}\"\"\"
            """

            resultado_mistral = mistral_service.classify_document(prompt)
            logging.info(f"✅ Resposta do Mistral para {file.filename}: {resultado_mistral}")

            resultado = {
                "arquivo": file.filename,
                "resultado": resultado_mistral
            }
            resultados.append(resultado)

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail=f"Arquivo JSON inválido: {file.filename}.")
        except Exception as e:
            logging.error(f"❌ Erro ao processar {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao processar {file.filename}: {str(e)}")

    # salva no arquivo JSON ( ainda nao finalizado )
    salvar_resultados(resultados, nome_arquivo)

    return resultados