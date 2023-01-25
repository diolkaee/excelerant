import json


def buildTemperatureEvent(temperatureC, chamber):
    return json.dumps({
        "chamber": chamber,
        "type": "temperature",
        "value": temperatureC
    })


def buildHumidityEvent(humidity, chamber):
    return json.dumps({
        "chamber": chamber,
        "type": "humidity",
        "value": humidity
    })


def buildExposureEvent(exposure, chamber):
    return json.dumps({
        "chamber": chamber,
        "type": "exposure",
        "value": exposure
    })


def buildPowerEvent(hasPower, chamber):
    return json.dumps({
        "chamber": chamber,
        "type": "power",
        "value": hasPower
    })


def buildFanSpeedEvent(fanSpeed):
    return json.dumps({
        "type": "fanspeed",
        "value": fanSpeed
    })
