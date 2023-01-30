import asyncio
from typing import Awaitable, Callable, Optional, Tuple
from datetime import datetime, time

from .core import ExcelerantCore, is_time_between
from .observer import buildObserver

__author__ = "Eike Meyer"
__version__ = "0.1.0"


class Excelerant(ExcelerantCore):
    def __init__(self):
        super(ExcelerantCore, self).__init__()
        # Activate indoor humidity sensor
        self._pixtend.gpio0_ctrl = 3
        self._pixtend.gpio0 = True
        # Activate indoor temperature sensor
        self._pixtend.gpio1_ctrl = 3
        self._pixtend.gpio1 = True
        # Activate light timers
        self.growTimer = True
        self.bloomTimer = True

    def getFanPower(self) -> bool:
        return self._pixtend.relay0

    def setFanPower(self, power: bool):
        self._pixtend.relay0 = power or (
            self.isGrowLightOn() or self.isBloomLightOn())

    def setFanSpeed(self, percent: float):
        # Fan speed ranges from 0.0 (0V) to 1.0 (10V). Input accepts 0..1023
        speed = 1023 * percent
        # If at least one light is on, set minimum speed to ~30%
        if ((self.isGrowLightOn() or self.isBloomLightOn()) and speed < 300):
            speed = 300
        self._pixtend.analog_out0 = speed

    def getFanSpeed(self) -> float:
        return self._pixtend.analog_out0

    async def observeFanSpeed(self, onFanSpeedChange: Callable[[float], Awaitable[None]]):
        fanObserver = buildObserver(self.getFanSpeed)
        await fanObserver(onFanSpeedChange)

    def isGrowLightOn(self) -> bool:
        return self._pixtend.relay1

    def setGrowLight(self, power: bool):
        self._pixtend.relay1 = power

    async def observeGrowLight(self, onGrowLightChange: Callable[[bool], Awaitable[None]]):
        growLightObserver = buildObserver(self.isGrowLightOn)
        await growLightObserver(onGrowLightChange)

    def isBloomLightOn(self) -> bool:
        return self._pixtend.relay2

    def setBloomLight(self, power: bool):
        self._pixtend.relay2 = power

    async def observeBloomLight(self, onBloomLightChange: Callable[[bool], Awaitable[None]]):
        bloomLightObserver = buildObserver(self.isBloomLightOn)
        await bloomLightObserver(onBloomLightChange)

    def getGrowHumidity(self) -> float:
        return self._pixtend.humid0

    async def observeGrowHumidity(self, onGrowHumidityChange: Callable[[float], Awaitable[None]]):
        growHumidityObserver = buildObserver(self.getGrowHumidity)
        await growHumidityObserver(onGrowHumidityChange)

    def getBloomHumidity(self) -> float:
        return self._pixtend.humid1

    async def observeBloomHumidity(self, onBloomHumidityChange: Callable[[float], Awaitable[None]]):
        bloomHumidityObserver = buildObserver(self.getBloomHumidity)
        await bloomHumidityObserver(onBloomHumidityChange)

    def getGrowTemperature(self) -> float:
        return self._pixtend.temp0

    async def observeGrowTemperature(self, onGrowTemperatureChange: Callable[[float], Awaitable[None]]):
        growTemperatureObserver = buildObserver(self.getGrowTemperature)
        await growTemperatureObserver(onGrowTemperatureChange)

    def getBloomTemperature(self) -> float:
        return self._pixtend.temp1

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
