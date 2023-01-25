import asyncio
import time
from pixtendv2s import PiXtendV2S

pixtend = None


def init():
    global pixtend
    pixtend = PiXtendV2S()
    # Activate indoor humidity sensor
    pixtend.gpio0_ctrl = 3
    pixtend.gpio0 = True
    # Activate indoor temperature sensor
    pixtend.gpio1_ctrl = 3
    pixtend.gpio1 = True


def setFanPower(hasPower):
    global pixtend
    pixtend.relay0 = hasPower


def setFanSpeed(percent):
    global pixtend
    # Fan speed ranges from 0.0 (0V) to 1.0 (10V). Input accepts 0..1023
    speed = 1023 * percent
    pixtend.analog_out0 = speed


def getFanSpeed():
    return pixtend.analog_out0


def setGrowLight(hasPower):
    global pixtend
    pixtend.relay1 = hasPower


def getGrowLight():
    return pixtend.relay1


def setBloomLight(hasPower):
    global pixtend
    pixtend.relay2 = hasPower


def getBloomLight():
    return pixtend.relay2


def getGrowHumidity():
    return pixtend.humid0


def getBloomHumidity():
    return pixtend.humid1


def getGrowTemperature():
    return pixtend.temp0


def getBloomTemperature():
    return pixtend.temp1


async def observeFanSpeed(onFanSpeedChange):
    lastFanSpeed = 0

    while (True):
        currentFanSpeed = getFanSpeed()
        if (currentFanSpeed != lastFanSpeed):
            onFanSpeedChange(currentFanSpeed)
            lastFanSpeed = currentFanSpeed
        time.sleep(1)


async def observeGrowLight(onGrowLightChange):
    lastGrowLight = False

    while (True):
        currentGrowLight = getGrowLight()
        if (currentGrowLight != lastGrowLight):
            onGrowLightChange(currentGrowLight)
            lastGrowLight = currentGrowLight
        time.sleep(1)
