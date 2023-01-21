import asyncio
import os
from random import randrange
import websockets

from input import handleEvent
from output import buildHumidityEvent, buildTemperatureEvent

PORT = os.environ.get('PORT') or 8765

CONNECTION = None


async def handler(websocket):
    await asyncio.gather(
        handleConnection(websocket),
        sendExampleData(websocket)
    )


async def handleConnection(websocket):
    global CONNECTION
    try:
        CONNECTION = websocket
        async for message in websocket:
            handleEvent(message)
    finally:
        CONNECTION = None


async def sendExampleData(websocket):
    while True:
        await websocket.send(buildTemperatureEvent(randrange(40)))
        await websocket.send(buildHumidityEvent(randrange(20)))
        await asyncio.sleep(2)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
