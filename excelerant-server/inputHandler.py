import json


def parseEvent(event):
    jsonData = json.loads(event)

    eventChamber = jsonData['chamber'] if 'chamber' in jsonData else None

    eventType = jsonData['type']
    if eventType is None:
        print("No event type given")

    eventValue = jsonData['value']
    if eventValue is None:
        print("No event value given")

    return [eventType, eventValue, eventChamber]


def handleEvent(event, state):
    [type, value, chamber] = parseEvent(event)
    match type:
        case 'temperature':
            handleTemperatureInput(value, chamber, state)
        case 'humidity':
            handleHumidityInput(value, chamber, state)
        case 'power':
            handlePowerChange(value, chamber, state)
        case 'exposure':
            handleExposure(value, chamber, state)
        case 'fanSpeed':
            handleFanSpeedChange(value, state)


def handleTemperatureInput(temperature, chamber, state):
    key = 'growTemperature' if chamber == 'grow' else 'bloomTemperature'
    state[key] = temperature
    print(f'Received {key}: {temperature}')


def handleHumidityInput(humidity, chamber, state):
    key = 'growHumidity' if chamber == 'grow' else 'bloomHumidity'
    state[key] = humidity
    print(f'Received {key}: {humidity}')


def handlePowerChange(isPowered, chamber, state):
    key = 'growPower' if chamber == 'grow' else 'bloomPower'
    state[key] = isPowered
    print(f'Received {key}: {isPowered}')


def handleExposure(exposure, chamber, state):
    key = 'growExposure' if chamber == 'grow' else 'bloomExposure'
    state[key] = exposure
    print(f'Received {key}: {exposure}')


def handleFanSpeedChange(fanSpeed, state):
    state['fanSpeed'] = fanSpeed
    print(f'Received fan speed: {fanSpeed}')
