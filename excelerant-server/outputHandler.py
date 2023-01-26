import asyncio
import json
from typing import Awaitable, Callable, Literal

from pixtendController import observeBloomHumidity, observeBloomLight, observeBloomTemperature, observeFanSpeed, observeGrowHumidity, observeGrowLight, observeGrowTemperature

ChamberType = Literal['grow', 'bloom']


def buildTemperatureEvent(temperatureC: float, chamber: ChamberType) -> str:
    return json.dumps({
        "chamber": chamber,
        "type": "temperature",
        "value": temperatureC
    })


def buildHumidityEvent(humidity: float, chamber: ChamberType) -> str:
    return json.dumps({
        "chamber": chamber,
        "type": "humidity",
        "value": humidity
    })


def buildExposureEvent(exposure, chamber: ChamberType) -> str:
    # FIXME Type me
    return json.dumps({
        "chamber": chamber,
        "type": "exposure",
        "value": exposure
    })


def buildPowerEvent(hasPower: bool, chamber: ChamberType) -> str:
    return json.dumps({
        "chamber": chamber,
        "type": "power",
        "value": hasPower
    })


def buildFanSpeedEvent(fanSpeed: float) -> str:
    return json.dumps({
        "type": "fanspeed",
        "value": fanSpeed
    })


async def observePixtend(onEvent: Callable[[str], Awaitable[None]]):
    async def onFanSpeedChange(fanSpeed: float): await onEvent(
        buildFanSpeedEvent(fanSpeed))

    async def onGrowLightChange(growLight: bool): await onEvent(
        buildPowerEvent(growLight, 'grow'))

    async def onBloomLightChange(bloomLight: bool): await onEvent(
        buildPowerEvent(bloomLight, 'bloom'))

    async def onGrowHumidityChange(growHumidity: float): await onEvent(
        buildHumidityEvent(growHumidity, 'grow'))

    async def onBloomHumidityChange(bloomHumidity: float): await onEvent(
        buildHumidityEvent(bloomHumidity, 'bloom'))

    async def onGrowTemperatureChange(growTemperature: float): await onEvent(
        buildTemperatureEvent(growTemperature, 'grow'))

    async def onBloomTemperatureChange(bloomTemperature: float): await onEvent(
        buildTemperatureEvent(bloomTemperature, 'bloom'))

    fanSpeedTask = asyncio.create_task(observeFanSpeed(onFanSpeedChange))
    growLightTask = asyncio.create_task(observeGrowLight(onGrowLightChange))
    bloomLightTask = asyncio.create_task(observeBloomLight(onBloomLightChange))
    growHumidityTask = asyncio.create_task(
        observeGrowHumidity(onGrowHumidityChange))
    bloomHumidityTask = asyncio.create_task(
        observeBloomHumidity(onBloomHumidityChange))
    growTemperatureTask = asyncio.create_task(
        observeGrowTemperature(onGrowTemperatureChange))
    bloomTemperatureTask = asyncio.create_task(
        observeBloomTemperature(onBloomTemperatureChange))

    await fanSpeedTask
    await growLightTask
    await bloomLightTask
    await growHumidityTask
    await bloomHumidityTask
    await growTemperatureTask
    await bloomTemperatureTask
