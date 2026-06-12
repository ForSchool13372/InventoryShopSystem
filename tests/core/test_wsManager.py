import pytest
from unittest.mock import AsyncMock

from app.core.wsManager import WSManager


@pytest.mark.asyncio
async def test_connect():
    manager = WSManager()

    ws = AsyncMock()

    await manager.connect(ws)

    ws.accept.assert_awaited_once()
    assert ws in manager.activeConnections


def test_disconnect():
    manager = WSManager()

    ws = AsyncMock()
    manager.activeConnections.add(ws)

    manager.disconnect(ws)

    assert ws not in manager.activeConnections


@pytest.mark.asyncio
async def test_broadcast():
    manager = WSManager()

    ws1 = AsyncMock()
    ws2 = AsyncMock()

    manager.activeConnections.add(ws1)
    manager.activeConnections.add(ws2)

    data = {"msg": "hello"}

    await manager.broadcast(data)

    ws1.send_json.assert_awaited_once_with(data)
    ws2.send_json.assert_awaited_once_with(data)


@pytest.mark.asyncio
async def test_broadcast_no_connections():
    manager = WSManager()

    await manager.broadcast({"msg": "hello"})

    assert len(manager.activeConnections) == 0


@pytest.mark.asyncio
async def test_broadcast_removes_dead_connections():
    manager = WSManager()

    goodWs = AsyncMock()
    badWs = AsyncMock()

    badWs.send_json.side_effect = Exception("dead connection")

    manager.activeConnections.add(goodWs)
    manager.activeConnections.add(badWs)

    await manager.broadcast({"msg": "hello"})

    assert goodWs in manager.activeConnections
    assert badWs not in manager.activeConnections


@pytest.mark.asyncio
async def test_broadcast_leaderboard():
    manager = WSManager()

    manager.broadcast = AsyncMock()

    leaderboard = [{"player": "Bob", "gold": 100}]

    await manager.broadcastLeaderboard(leaderboard)

    manager.broadcast.assert_awaited_once_with({
        "type": "LEADERBOARD_UPDATE",
        "data": leaderboard
    })