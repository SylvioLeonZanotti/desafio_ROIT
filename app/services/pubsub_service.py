import logging

logging.basicConfig(level=logging.INFO)

#não deu certo por conta da conta do google cloud
class PubSubService:
    def __init__(self):

        self.topics = {}

    def publish_message(self, topic: str, message: dict):

        if topic not in self.topics:
            self.topics[topic] = []

        self.topics[topic].append(message)
        logging.info(f"✅ Mensagem publicada no tópico '{topic}': {message}")
        return {"status": "Mensagem publicada", "topic": topic, "message": message}

    def subscribe_messages(self, topic: str):

        if topic in self.topics:
            messages = self.topics[topic]
            logging.info(f"✅ Mensagens recuperadas do tópico '{topic}': {messages}")
            return {"status": "Mensagens recuperadas", "topic": topic, "messages": messages}

        logging.warning(f"⚠ Nenhuma mensagem encontrada no tópico '{topic}'")
        return {"status": "Nenhuma mensagem encontrada", "topic": topic, "messages": []}

# instância do serviço
pubsub_service = PubSubService()
