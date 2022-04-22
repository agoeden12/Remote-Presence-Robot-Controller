import asyncio
import websockets
from time import sleep
import json

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(json.dumps([0,1]))
        

while True:
    asyncio.run(hello())
    sleep(1)