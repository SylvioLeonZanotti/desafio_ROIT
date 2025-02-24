import os
import requests
import mimetypes

# script para enviar mais arquivos por conta do limite do postman
API_URL = "http://localhost:8000/classify/upload"  
PASTA_ARQUIVOS = r"C:\Users\ozanotti\Desktop\desafio\dataset\boleto\boletos_teste"  

def enviar_arquivos():
    arquivos = []
    # for pra percorrer todos os arquivos
    for filename in os.listdir(PASTA_ARQUIVOS):
        caminho_arquivo = os.path.join(PASTA_ARQUIVOS, filename)
        
        if os.path.isfile(caminho_arquivo):
            content_type, _ = mimetypes.guess_type(caminho_arquivo)
            if content_type is None:
                print(f"tipo de arquivo não detectado para {filename}, enviando como 'application/octet-stream'.")
                content_type = "application/octet-stream"

            arquivos.append(("files", (filename, open(caminho_arquivo, "rb"), content_type)))

    if not arquivos:
        print("Nenhum arquivo encontrado na pasta.")
        return

    print(f"enviando {len(arquivos)} arquivos para a API...")

    response = requests.post(API_URL, files=arquivos, params={"nome_arquivo": "boletos.json"})

    for _, (name, file, _) in arquivos:
        file.close()

    if response.status_code == 200:
        print("Envio concluído com sucesso!")
        print(response.json())  # Mostra a resposta da API
    else:
        print(f"Erro ao enviar arquivos: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    enviar_arquivos()
