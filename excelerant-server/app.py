import asyncio
import os
import websockets

from inputHandler import handleEvent
from outputHandler import observePixtend
from pixtendController import closePixtend, initPixtend

PORT = os.environ.get('PORT') or 8765

CONNECTION = None


async def handler(websocket):
    await asyncio.gather(
        handleConnection(websocket),
        handleUpdates(websocket)
    )


async def handleConnection(websocket):
    global CONNECTION
    try:
        CONNECTION = websocket
        initPixtend()
        async for message in websocket:
            handleEvent(message)
    finally:
        CONNECTION = None
        closePixtend()


async def handleUpdates(websocket):
    async def onUpdate(event: str): return await websocket.send(event)
    await observePixtend(onUpdate)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        print(f'Starting excelerant server on Port: {PORT}')
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
