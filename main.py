"""
Backend FastAPI com WebSocket para chat em tempo real.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Set
import json
import logging
import os
from pathlib import Path

from chat_handler import ChatHandler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chat App API", version="1.0.0")

# Configurar CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerenciador de chat
chat_handler = ChatHandler()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Chat App API is running",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "/ws/{user_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "connections": len(manager.active_connections) if 'manager' in globals() else 0
    }

# Endpoint de teste via HTTP (útil para automação/cURL)
@app.get("/test")
async def test_get(mensagem: str, user_id: str = "teste"):
    resposta = chat_handler.processar_mensagem(user_id, mensagem)
    return resposta

@app.post("/test")
async def test_post(payload: dict):
    user_id = payload.get("user_id", "teste")
    mensagem = payload.get("mensagem", "")
    resposta = chat_handler.processar_mensagem(user_id, mensagem)
    return resposta

# Armazena conexões WebSocket ativas
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"✅ Usuário {user_id} conectado. Total: {len(self.active_connections)}")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"❌ Usuário {user_id} desconectado. Total: {len(self.active_connections)}")
    
    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "app": "Chat App API",
        "version": "1.0.0",
        "status": "online",
        "conexoes_ativas": len(manager.active_connections)
    }


@app.get("/health")
async def health_check():
    """Health check."""
    return {
        "status": "healthy",
        "conexoes_ativas": len(manager.active_connections)
    }


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    Endpoint WebSocket para comunicação em tempo real.
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Mensagem de boas-vindas
        await manager.send_message(user_id, {
            "tipo": "sistema",
            "texto": "🟢 Conectado ao servidor!",
            "timestamp": ""
        })
        
        while True:
            # Recebe mensagem do cliente
            data = await websocket.receive_text()
            mensagem_data = json.loads(data)
            
            mensagem_texto = mensagem_data.get("mensagem", "")
            logger.info(f"📨 Mensagem de {user_id}: {mensagem_texto}")
            
            # Processa a mensagem
            resposta = chat_handler.processar_mensagem(user_id, mensagem_texto)
            
            # Envia resposta
            await manager.send_message(user_id, {
                "tipo": "resposta",
                "texto": resposta["texto"],
                "categoria": resposta["tipo"],
                "timestamp": ""
            })
            
            logger.info(f"📤 Resposta enviada para {user_id}")
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"🔴 WebSocket desconectado: {user_id}")
    
    except Exception as e:
        logger.error(f"❌ Erro no WebSocket: {e}", exc_info=True)
        manager.disconnect(user_id)


# Configuração para Railway - detecta porta automaticamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
