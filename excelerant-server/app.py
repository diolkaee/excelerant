import asyncio
import os
import websockets

from inputHandler import handleEvent
from outputHandler import buildExposureEvent, buildFanSpeed, buildFanSpeedEvent, buildHumidityEvent, buildPowerEvent, buildTemperatureEvent
from pixtendController import init, observeFanSpeed

PORT = os.environ.get('PORT') or 8765

CONNECTION = None

state = {
    'growTemperature': 0,
    'bloomTemperature': 0,
    'growHumidity': 0,
    'bloomHumdity': 0,
    'growExposure': {"start": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}},
    'bloomExposure': {"start": {"hour": 0, "minute": 0}, "end": {"hour": 0, "minute": 0}},
    'growPower': False,
    'bloomPower': False,
    'fanSpeed': 0
}


async def handler(websocket):
    await asyncio.gather(
        handleConnection(websocket),
        observePixtend(websocket)
    )


async def handleConnection(websocket):
    global CONNECTION, state
    try:
        CONNECTION = websocket
        async for message in websocket:
            handleEvent(message, state)
    finally:
        CONNECTION = None


async def observePixtend(websocket):
    async def onFanSpeedChange(fanSpeed): return await websocket.send(
        buildFanSpeedEvent(fanSpeed))
    observeFanSpeed(onFanSpeedChange)


async def main():
    init()
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
