import asyncio
import os
from random import randrange
import websockets

from input import handleEvent
from output import buildExposureEvent, buildFanSpeed, buildHumidityEvent, buildPowerEvent, buildTemperatureEvent

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
        sendExampleData(websocket)
    )


async def handleConnection(websocket):
    global CONNECTION, state
    try:
        CONNECTION = websocket
        async for message in websocket:
            handleEvent(message, state)
    finally:
        CONNECTION = None


async def sendExampleData(websocket):
    while True:
        await websocket.send(buildTemperatureEvent(state['growTemperature'], 'grow'))
        await websocket.send(buildTemperatureEvent(state['bloomTemperature'], 'bloom'))
        await websocket.send(buildHumidityEvent(state['growHumidity'], 'grow'))
        await websocket.send(buildHumidityEvent(state['bloomHumdity'], 'bloom'))
        await websocket.send(buildExposureEvent(state['growExposure'], 'grow'))
        await websocket.send(buildExposureEvent(state['bloomExposure'], 'bloom'))
        await websocket.send(buildPowerEvent(state['growPower'], 'grow'))
        await websocket.send(buildPowerEvent(state['bloomPower'], 'bloom'))
        await websocket.send(buildFanSpeed(state['fanSpeed']))
        await asyncio.sleep(2)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
