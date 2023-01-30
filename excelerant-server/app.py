import asyncio
import os
import websockets

from excelerant import Excelerant
from inputHandler import handleEvent
from outputHandler import observeExcelerant

PORT = os.environ.get('PORT') or 8765

CONNECTION = None


async def handler(websocket):
    excelerant = Excelerant()
    with excelerant:
        await asyncio.gather(
            handleConnection(excelerant, websocket),
            handleUpdates(excelerant, websocket)
        )


async def handleConnection(excelerant, websocket):
    global CONNECTION
    try:
        CONNECTION = websocket
        async for message in websocket:
            handleEvent(excelerant, message)
    finally:
        CONNECTION = None


async def handleUpdates(excelerant, websocket):
    async def onUpdate(event: str): return await websocket.send(event)
    await observeExcelerant(excelerant, onUpdate)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        print(f'Starting excelerant server on Port: {PORT}')
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
