import asyncio
import websockets
import json

async def test():
    uri = "ws://127.0.0.1:8000/api/ws/leaderboard"

    async with websockets.connect(uri) as ws:
        while True:
            msg = await ws.recv()
            print(json.loads(msg))

asyncio.run(test())
