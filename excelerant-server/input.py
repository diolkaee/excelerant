import json


def parseEvent(event):
    jsonData = json.loads(event)
    eventType = jsonData['type']
    if eventType is None:
        print("No event type given")

    eventValue = jsonData['value']
    if eventValue is None:
        print("No event value given")
    return [eventType, eventValue]


def handleEvent(event):
    [type, value] = parseEvent(event)
    match type:
        case 'temperature':
            handleTemperatureInput(value)
        case 'humidity':
            handleHumidityInput(value)


def handleTemperatureInput(temperature):
    print(f'Received temperature: {temperature}')


def handleHumidityInput(humidity):
    print(f'Received humidity: {humidity}')
