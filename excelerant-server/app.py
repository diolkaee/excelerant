import asyncio
import os
import websockets

PORT = os.environ.get('PORT') or 8765


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with websockets.serve(echo, "localhost", PORT):
        await asyncio.Future()

asyncio.run(main())
