import requests
import json
import logging

class MistralService:
    def __init__(self, url="http://host.docker.internal:1234/v1/chat/completions"): # levar pro config se der tempo
        self.url = url

    def classify_document(self, text):

        if not text.strip():
            logging.warning("Texto vazio recebido para classificação.")
            return {
                "classificacao": "Não especificado",
                "cnpj": "Não encontrado",
                "codigo_barras": "Não encontrado",
                "valor_total": "Não encontrado",
                "data_emissao": "Não encontrado",
                "numero_nf": "Não encontrado",
                "codigo_servico": "Não encontrado",
                "agencia": "Não encontrado",
                "conta": "Não encontrado",
                "valor_transacao": "Não encontrado",
                "data_operacao": "Não encontrado"
            }

        prompt = f"""
        Você é um assistente especializado em extração de informações de documentos financeiros.
        Seu objetivo é analisar o texto e responder **somente** com um JSON válido.

        **Instruções:**
        - Se for um **Boleto**, extraia:
          - "cnpj": O CNPJ do emissor do boleto (sempre no formato `XX.XXX.XXX/XXXX-XX`).
          - "codigo_barras": O número do código de barras (44 ou 48 dígitos, sem espaços).
          - "valor_boleto": O valor total do boleto (exemplo: `"R$ 150,00"`).
          - "data_vencimento": A data de vencimento do boleto no formato `DD/MM/AAAA`.

        - Se for uma **Nota Fiscal de Serviço Eletrônica (NFSe)**, extraia:
          - "cnpj_emitente": O CNPJ do emissor da NFSe (formato `XX.XXX.XXX/XXXX-XX`).
          - "cnpj_tomador": O CNPJ do tomador do serviço (formato `XX.XXX.XXX/XXXX-XX`).
          - "valor_total": O valor total da nota fiscal (sempre em reais, ex: `"R$ 1.500,00"`).
          - "data_emissao": A data de emissão da nota fiscal no formato `DD/MM/AAAA`.
          - "numero_nf": O número da nota fiscal (somente números).
          - "codigo_servico": O código do serviço prestado.

        - Se for um **Comprovante**, extraia:
          - "cnpj_cpf": O CNPJ ou CPF associado ao pagamento.
          - "agencia": O número da agência bancária (somente números).
          - "conta": O número da conta bancária (somente números, incluir dígito).
          - "valor_transacao": O valor total da transação (exemplo: `"R$ 250,00"`).
          - "data_operacao": A data da operação no formato `DD/MM/AAAA`.

        **Formato esperado da resposta:**
        ```json
        {{
            "classificacao": "boleto",
            "cnpj": "XX.XXX.XXX/XXXX-XX",
            "codigo_barras": "12345678901234567890123456789012345678901234",
            "valor_boleto": "R$ 150,00",
            "data_vencimento": "10/03/2024"
        }}

        {{
            "classificacao": "nota fiscal",
            "cnpj_emitente": "XX.XXX.XXX/XXXX-XX",
            "cnpj_tomador": "YY.YYY.YYY/YYYY-YY",
            "valor_total": "R$ 1.500,00",
            "data_emissao": "10/02/2024",
            "numero_nf": "123456",
            "codigo_servico": "1201"
        }}

        {{
            "classificacao": "comprovante",
            "cnpj_cpf": "XXX.XXX.XXX-XX",
            "agencia": "1234",
            "conta": "56789-0",
            "valor_transacao": "R$ 250,00",
            "data_operacao": "05/03/2024"
        }}
        ```

        **Se algum campo não existir no documento, retorne `"Não encontrado"` em vez de deixá-lo vazio.**
        **Responda estritamente no formato JSON, sem explicações adicionais, sem texto fora do JSON.**

        **Texto extraído do documento:**
        \"\"\"{text}\"\"\"
        """

        payload = {
            "model": "mistral-7b-instruct-v0.3",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 250,
            "temperature": 0.2
        }

        try:
            response = requests.post(self.url, json=payload, timeout=15)

            if response.status_code == 200:
                raw_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                raw_response = raw_response.strip("`json").strip("`").strip()

                logging.info(f"✅ Resposta bruta do Mistral: {raw_response}")

                try:
                    parsed_response = json.loads(raw_response)
                    return parsed_response
                except json.JSONDecodeError:
                    logging.error("❌ O Mistral retornou um JSON inválido.")
                    return {"erro": "A resposta do Mistral não é um JSON válido"}

            else:
                logging.error(f"❌ Erro na requisição ao Mistral: {response.status_code} - {response.text}")
                return {"erro": "Erro na resposta do Mistral"}

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erro ao conectar com o Mistral: {e}")
            return {"erro": "Falha na conexão com Mistral"}

# instância do serviço
mistral_service = MistralService() 
