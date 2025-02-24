import json
import os

def salvar_resultados(resultados, nome_arquivo="boletos.json"):

    caminho_completo = os.path.join(os.getcwd(), nome_arquivo) 
    try:
        
        if os.path.exists(caminho_completo):
            with open(caminho_completo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        else:
            dados = []  

        dados.extend(resultados)

        with open(caminho_completo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        print(f"salvo em: {caminho_completo}")  

    except Exception as e:
        print(f"erro ao tentar salvar resultados: {e}")