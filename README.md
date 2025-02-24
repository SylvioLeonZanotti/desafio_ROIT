# 📌 Desafio ROIT - API de Classificação e Extração de Dados

## 📌 Visão Geral
Esta API foi desenvolvida para **classificar e extrair informações** de documentos financeiros como **boletos, notas fiscais e comprovantes**. Utiliza **OCR (Tesseract)** para processar imagens e PDFs, e o modelo **Mistral 7B** para interpretar o conteúdo extraído. Os resultados são salvos em arquivos JSON para futura consulta.

---

## 🚀 Tecnologias Utilizadas
- **FastAPI** - Framework para desenvolvimento da API
- **Mistral 7B** - Modelo de linguagem para interpretação de documentos ( Usando LMSTudio localmente )
- **Tesseract OCR** - Extração de texto de imagens e PDFs
- **Docker** - Contêinerização do projeto
- **Google Cloud Pub/Sub** - Mensageria para processamento assíncrono (simulado localmente não deu certo por conta da conta do google cloud)

---

## 🛠 Como Configurar e Rodar o Projeto

### 📌 **Rodar usando Docker** 
```sh
# 1. Construir a imagem
docker build -t desafio_roit .

# 2. Rodar o contêiner
docker run -p 8000:8000 desafio_roit
```

---

## 📂 Estrutura do Projeto
```plaintext
DESAFIO_ROIT/
├── app/
│   ├── api/
│   │   ├── routes/             # Rotas da API
│   │   │   ├── classification.py  # Rota para classificação de documentos
│   │   │   ├── extraction.py      # Rota para extração de texto
│   │   │   ├── pubsub.py          # Rota para publicação/assinatura no Pub/Sub
│   ├── services/            # Serviços internos
│   │   ├── classifier.py       # Classifica documentos
│   │   ├── extractor.py        # Processa arquivos PDF e imagens
│   │   ├── mistral_service.py  # Interface com o Mistral 7B
│   │   ├── ocr_service.py      # Extração de texto (OCR)
│   │   ├── pubsub_service.py   # Serviço de Pub/Sub (simulado localmente)
│   │   ├── storage_service.py  # Salva os resultados extraídos
├── tests/                      # Resultados de testes de extrações e classificações
├── main.py                     # Arquivo principal da API
├── Dockerfile                  # Configuração do Docker
├── requirements.txt            # Dependências do projeto
```

---

## ⚙️ Endpoints da API
### 📌 **Classificação de Documentos**
```http
POST /classify/upload
```
- **Entrada:** Arquivos JSON, PDF, JPEG ou `.pb.gz`
- **Saída:** Classificação do documento e extração de informações

### 📌 **Extração de Texto**
```http
POST /extract_text
```
- **Entrada:** Arquivo de imagem ou PDF
- **Saída:** Texto extraído

### 📌 **Publicação no Pub/Sub**
```http
POST /publish
```
- **Entrada:** Mensagem JSON
- **Saída:** Confirmação de publicação

### 📌 **Consulta de Mensagens do Pub/Sub**
```http
GET /subscribe
```
- **Entrada:** Nome do tópico
- **Saída:** Lista de mensagens publicadas

---

## 📊 Tipos de Documentos Suportados
### ✅ **Boleto**
- CNPJ do emissor
- Código de barras
- Valor do boleto
- Data de vencimento

### ✅ **NFSe (Nota Fiscal de Serviço Eletrônica)**
- CNPJ do emitente
- CNPJ do tomador
- Valor total
- Data de emissão
- Número da nota fiscal
- Código de serviço

### ✅ **Comprovante de Pagamento**
- CNPJ/CPF
- Número da agência
- Número da conta
- Valor da transação
- Data da operação

---

## 📁 Armazenamento de Resultados
Os resultados são armazenados em arquivos JSON na pasta tests que esta na pasta raiz separados por:
- `boletos.json` → Resultados de boletos
- `nfse.json` → Resultados de notas fiscais
- `comprovantes.json` → Resultados de comprovantes