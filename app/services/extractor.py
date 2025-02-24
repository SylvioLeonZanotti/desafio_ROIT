import logging
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf
from app.services.classifier import DocumentClassifier

logging.basicConfig(level=logging.INFO)

# função pra extrarir o texto do arquivo e classificar o conteudo
class DocumentExtractor:
    def __init__(self):
        self.classifier = DocumentClassifier()

    def extract_and_classify(self, file_bytes: bytes, file_type: str):

        extracted_text = None

        try:
            if file_type.startswith("image/"):
                logging.info("Extraindo texto de imagem via OCR...")
                extracted_text = extract_text_from_image(file_bytes)

            elif file_type == "application/pdf":
                logging.info("Extraindo texto de PDF...")
                extracted_text = extract_text_from_pdf(file_bytes)

            else:
                logging.warning("Tipo de arquivo não suportado")
                #retorna um padrão pra corrigir erro no retorno do json e api fechar
                return {
                    "classificacao": "Não suportado",
                    "cnpj": "Não identificado",
                    "codigo_barras": "Não identificado"
                }

            if not extracted_text:
                logging.warning("Nenhum texto extraído do documento.")
                return {
                    "classificacao": "Texto não detectado",
                    "cnpj": "Não identificado",
                    "codigo_barras": "Não identificado"
                }

            # classifica o documento com base no texto extraido
            resultado = self.classifier.classify(extracted_text)
            return resultado

        except Exception as e:
            logging.error(f"❌ Erro ao processar documento: {e}")
            return {
                "classificacao": "Erro no processamento",
                "cnpj": "Erro",
                "codigo_barras": "Erro"
            }
