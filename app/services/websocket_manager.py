from typing import Dict, List
from fastapi import WebSocket
import redis.asyncio as redis
import asyncio
from ..config import settings
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def connect(self, websocket: WebSocket, item_id: int):
        await websocket.accept()
        if item_id not in self.active_connections:
            self.active_connections[item_id] = []
        self.active_connections[item_id].append(websocket)

    def disconnect(self, websocket: WebSocket, item_id: int):
        self.active_connections[item_id].remove(websocket)
        if not self.active_connections[item_id]:
            del self.active_connections[item_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, item_id: int, message: str):
        if item_id in self.active_connections:
            for connection in self.active_connections[item_id]:
                await connection.send_text(message)

    async def pubsub_listener(self):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe("item_updates")
        print("Subscribed to Redis 'item_updates' channel")
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                item_id = data.get("item_id")
                item_data = data.get("item_data")
                if item_id and item_data:
                    print(f"Received update for item {item_id}: {item_data}")
                    await self.broadcast(item_id, json.dumps(item_data))
            await asyncio.sleep(0.01) # Small delay to prevent busy-waiting

manager = ConnectionManager()

async def start_websocket_manager():
    asyncio.create_task(manager.pubsub_listener())
