import pytest
from unittest.mock import AsyncMock
from app.infrastructure.logging.websocket_manager import WebSocketManager

@pytest.mark.asyncio
async def test_websocket_broadcast():
    manager = WebSocketManager()
    # On utilise AsyncMock car manager.connect appelle "await websocket.accept()"
    mock_ws = AsyncMock() 
    
    await manager.connect(mock_ws)
    
    mock_ws.accept.assert_called_once()