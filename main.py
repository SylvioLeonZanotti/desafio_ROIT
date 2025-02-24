from fastapi import FastAPI
from app.api.routes import classification, extraction, pubsub

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API desafio ROIT"}

# rotas dos módulos
app.include_router(classification.router, prefix="/classify", tags=["Classification"])
app.include_router(extraction.router, prefix="/extract", tags=["Extraction"])
app.include_router(pubsub.router, prefix="/pubsub", tags=["Pub/Sub"])
