from fastapi import APIRouter, HTTPException
import logging
from app.services.pubsub_service import pubsub_service  # 🔥 Certifique-se de que está importando a classe correta

logging.basicConfig(level=logging.INFO)
router = APIRouter()

# função pra publicar topico no google cloud
@router.post("/publish")
async def publish_to_pubsub(topic: str, message: dict):

    try:
        response = pubsub_service.publish_message(topic, message)  # 🔥 Chamada correta da instância
        logging.info(f"✅ Mensagem publicada no tópico {topic}: {message}")
        return {"status": "Mensagem publicada", "response": response}
    except Exception as e:
        logging.error(f"❌ Erro ao publicar no Pub/Sub: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao publicar no Pub/Sub: {str(e)}")

# função pra assinar topico no google cloud
@router.get("/subscribe")
async def subscribe_to_pubsub(topic: str):
    
    try:
        messages = pubsub_service.subscribe_messages(topic)  # 🔥 Chamada correta da instância
        logging.info(f"✅ Mensagens consumidas do tópico {topic}: {messages}")
        return {"mensagens": messages}
    except Exception as e:
        logging.error(f"❌ Erro ao assinar tópico Pub/Sub: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao assinar tópico Pub/Sub: {str(e)}")
