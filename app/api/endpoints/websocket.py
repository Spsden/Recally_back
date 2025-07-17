from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...services.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/items/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await manager.connect(websocket, item_id)
    try:
        while True:
            # Keep the connection alive, client can send messages if needed
            # For now, we just expect the server to push updates
            await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(websocket, item_id)
