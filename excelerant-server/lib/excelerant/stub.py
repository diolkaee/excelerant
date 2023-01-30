from ast import Tuple
import asyncio
from datetime import datetime, time
from typing import Awaitable, Callable, Optional

from .core import is_time_between
from .observer import buildObserver

__author__ = "Eike Meyer"
__version__ = "0.1.0"


class ExcelerantStub():
    def __init__(self):
        self.fanPower = 0
        self.fanSpeed = 0
        self.growLight = False
        self.bloomLight = False
        self.growHumidity = 0.0
        self.bloomHumidity = 0.0
        self.growTemperature = 0.0
        self.bloomTemperature = 0.0

    def __exit__(self):
        pass

    def getFanPower(self) -> bool:
        return self.fanPower

    def setFanPower(self, power: bool):
        self.fanPower = power

    def setFanSpeed(self, percent: float):
        # Fan speed ranges from 0.0 (0V) to 1.0 (10V). Input accepts 0..1023
        speed = 1023 * percent
        # If at least one light is on, set minimum speed to ~30%
        if ((self.isGrowLightOn() or self.isBloomLightOn()) and speed < 300):
            speed = 300
        self.fanSpeed = speed

    def getFanSpeed(self) -> float:
        return self.fanSpeed

    async def observeFanSpeed(self, onFanSpeedChange: Callable[[float], Awaitable[None]]):
        fanObserver = buildObserver(self.getFanSpeed)
        await fanObserver(onFanSpeedChange)

    def setGrowLight(self, power: bool):
        self.growLight = power

    def isGrowLightOn(self) -> bool:
        return self.growLight

    async def observeGrowLight(self, onGrowLightChange: Callable[[bool], Awaitable[None]]):
        growLightObserver = buildObserver(self.isGrowLightOn)
        await growLightObserver(onGrowLightChange)

    def setBloomLight(self, power: bool):
        self.bloomLight = power

    def isBloomLightOn(self) -> bool:
        return self.bloomLight

    async def observeBloomLight(self, onBloomLightChange: Callable[[bool], Awaitable[None]]):
        bloomLightObserver = buildObserver(self.isBloomLightOn)
        await bloomLightObserver(onBloomLightChange)

    def getGrowHumidity(self) -> float:
        return self.growHumidity

    async def observeGrowHumidity(self, onGrowHumidityChange: Callable[[float], Awaitable[None]]):
        growHumidityObserver = buildObserver(self.getGrowHumidity)
        await growHumidityObserver(onGrowHumidityChange)

    def getBloomHumidity(self) -> float:
        return self.bloomHumidity

    async def observeBloomHumidity(self, onBloomHumidityChange: Callable[[float], Awaitable[None]]):
        bloomHumidityObserver = buildObserver(self.getBloomHumidity)
        await bloomHumidityObserver(onBloomHumidityChange)

    def getGrowTemperature(self) -> float:
        return self.growTemperature

    async def observeGrowTemperature(self, onGrowTemperatureChange: Callable[[float], Awaitable[None]]):
        growTemperatureObserver = buildObserver(self.getGrowTemperature)
        await growTemperatureObserver(onGrowTemperatureChange)

    def getBloomTemperature(self) -> float:
        return self.bloomTemperature

    async def observeBloomTemperature(self, onBloomTemperatureChange: Callable[[float], Awaitable[None]]):
        bloomTemperatureObserver = buildObserver(self.getBloomTemperature)
        await bloomTemperatureObserver(onBloomTemperatureChange)

    def setGrowTime(self, start: time, end: time):
        self.growTime = (start, end)

    def getGrowTime(self) -> Optional[Tuple[time, time]]:
        return self.growTime

    async def controlGrowTime(self):
        while (True):
            if (self.growTimer):
                currentTime = datetime.now().time()
                if (self.growTime != None):
                    if (is_time_between(currentTime, self.growTime[0], self.growTime[1])):
                        self.setGrowLight(True)
                    else:
                        self.setGrowLight(False)
            else:
                pass
            await asyncio.sleep(30)

    def setBloomTime(self, start: time, end: time):
        self.bloomTime = (start, end)

    def getBloomTime(self) -> Optional[Tuple[time, time]]:
        return self.bloomTime

    async def controlBloomTime(self):
        while (True):
            if (self.bloomTimer):
                currentTime = datetime.datetime.now().time()
                if (self.bloomTime != None):
                    if (is_time_between(currentTime, self.bloomTime[0], self.bloomTime[1])):
                        self.setBloomLight(True)
                    else:
                        self.setBloomLight(False)
            await asyncio.sleep(30)
