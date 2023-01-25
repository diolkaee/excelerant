import asyncio
from datetime import datetime, time
from typing import Callable, Optional, Tuple
from pixtendv2s import PiXtendV2S

pixtend = None

growTime: Optional[Tuple[time, time]] = None
bloomTime = None


def init():
    global pixtend
    pixtend = PiXtendV2S()
    # Activate indoor humidity sensor
    pixtend.gpio0_ctrl = 3
    pixtend.gpio0 = True
    # Activate indoor temperature sensor
    pixtend.gpio1_ctrl = 3
    pixtend.gpio1 = True


def setFanPower(hasPower: bool):
    global pixtend
    pixtend.relay0 = hasPower or (getGrowLight() or getBloomLight())


def setFanSpeed(percent: float):
    global pixtend
    # Fan speed ranges from 0.0 (0V) to 1.0 (10V). Input accepts 0..1023
    speed = 1023 * percent
    # If at least one light is on, set minimum speed to ~30%
    if ((getGrowLight() or getBloomLight()) and speed < 300):
        speed = 300
    pixtend.analog_out0 = speed


async def observeFanSpeed(onFanSpeedChange: Callable[[float], None]):
    lastFanSpeed = 0

    while (True):
        currentFanSpeed = getFanSpeed()
        if (currentFanSpeed != lastFanSpeed):
            onFanSpeedChange(currentFanSpeed)
            lastFanSpeed = currentFanSpeed
        asyncio.sleep(1)


def getFanSpeed() -> float:
    return pixtend.analog_out0


def setGrowLight(hasPower: bool):
    global pixtend
    pixtend.relay1 = hasPower


def getGrowLight() -> bool:
    return pixtend.relay1


async def observeGrowLight(onGrowLightChange: Callable[[bool], None]):
    lastGrowLight = False

    while (True):
        currentGrowLight = getGrowLight()
        if (currentGrowLight != lastGrowLight):
            onGrowLightChange(currentGrowLight)
            lastGrowLight = currentGrowLight
        asyncio.sleep(1)


def setBloomLight(hasPower: bool):
    global pixtend
    pixtend.relay2 = hasPower


def getBloomLight() -> bool:
    return pixtend.relay2


def getGrowHumidity() -> float:
    return pixtend.humid0


def getBloomHumidity() -> float:
    return pixtend.humid1


def getGrowTemperature() -> float:
    return pixtend.temp0


def getBloomTemperature() -> float:
    return pixtend.temp1


def setGrowTime(start: time, end: time):
    # Set growtime
    global growTime
    growTime = (start, end)


def getGrowTime() -> Optional[Tuple[time, time]]:
    return growTime


async def controlGrowTime():
    global pixtend
    while (True):
        currentTime = datetime.datetime.now().time()
        if (growTime != None):
            if (is_time_between(currentTime, growTime[0], growTime[1])):
                setGrowLight(True)
            else:
                setGrowLight(False)
        asyncio.sleep(30)


def setBloomTime(start: time, end: time):
    # Set bloomtime
    global bloomTime
    bloomTime = (start, end)


def getBloomTime() -> Optional[Tuple[time, time]]:
    return bloomTime


async def controlBloomTime():
    global pixtend
    while (True):
        currentTime = datetime.datetime.now().time()
        if (bloomTime != None):
            if (is_time_between(currentTime, bloomTime[0], bloomTime[1])):
                setBloomLight(True)
            else:
                setBloomLight(False)
        asyncio.sleep(30)


def is_time_between(time: time, start: time, end: time) -> bool:
    if start <= end:
        return start <= time < end
    else:
        return start <= time or time < end
