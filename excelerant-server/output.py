import json


def buildTemperatureEvent(temperatureC):
    return json.dumps({
        "type": "temperature",
        "value": temperatureC
    })


def buildHumidityEvent(humidity):
    return json.dumps({
        "type": "humidity",
        "value": humidity
    })
