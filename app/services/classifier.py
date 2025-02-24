import logging
from app.services.mistral_service import mistral_service

logging.basicConfig(level=logging.INFO)

# função pra classificar os docs usando mistral 7b mas se não retornar nada ja retorna um json padrão
class DocumentClassifier:
    def __init__(self):
        self.mistral = mistral_service

    def classify(self, extracted_text: str):

        if not extracted_text.strip():
            return {
                "classificacao": "Não especificado",
                "cnpj": "Não encontrado",
                "codigo_barras": "Não encontrado"
            }

        try:
            # envia para o mistral pra analise
            resultado = self.mistral.classify_document(extracted_text)

            if isinstance(resultado, dict) and "classificacao" in resultado:
                return resultado
            else:
                logging.error("❌ Resposta inválida do Mistral. Retornando padrão.")
                return {
                    "classificacao": "Erro na classificação",
                    "cnpj": "Não encontrado",
                    "codigo_barras": "Não encontrado"
                }
        except Exception as e:
            logging.error(f"❌ Erro ao classificar documento: {str(e)}")
            return {
                "classificacao": "Erro na classificação",
                "cnpj": "Não encontrado",
                "codigo_barras": "Não encontrado"
            }

# instancia do classificador pra uso em outros modulos
document_classifier = DocumentClassifier()
